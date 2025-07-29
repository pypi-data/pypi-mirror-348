"""Functions for motif analysis in genomic data.

This module contains functions for analyzing transcription factor motifs
in genomic data, including computing motif scores and generating
in-silico ChIP-seq signals based on motif information.
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd
from beartype import beartype

logger = logging.getLogger(__name__)


@beartype
def compute_motif_scores(
    bed_file: Path,
    fasta_file: Path,
    pwms_sub: dict,
    key_to_tf: dict,
    n_peaks: int,
    window: int,
    threshold: float,
    batch_size_Fimo_scan: int,
) -> pd.DataFrame:
    """Extract sequences from genomic regions and compute motif scores.

    Uses the FIMO algorithm to scan motifs across sequences extracted from genomic regions
    defined in a BED file, and computes scores for matches. Results are returned as a
    DataFrame with peaks as rows and TFs as columns.

    Args:
        bed_file: Path to BED file containing genomic regions.
        fasta_file: Path to genome FASTA file.
        pwms_sub: Dictionary containing position weight matrices (PWMs) for motifs.
        key_to_tf: Dictionary mapping motif keys to TF names.
        n_peaks: Number of peaks to process.
        window: Size of window around peaks to scan for motifs (in base pairs).
        threshold: P-value threshold for motif matching.
        batch_size_Fimo_scan: Number of motifs to process in each FIMO call.

    Returns:
        DataFrame with shape (n_peaks, n_TFs), where rows are indexed by peak names
        and columns are TF names. Values are normalized motif scores between 0 and 1.
    """
    from sklearn.preprocessing import MinMaxScaler
    from tangermeme.io import extract_loci
    from tangermeme.tools.fimo import fimo
    from tqdm import tqdm

    # actual method
    logger.info(
        f"Computing motif scores for {bed_file} (n_peaks={n_peaks}) with window={window}"
    )
    loci = pd.read_csv(bed_file, sep="\t", header=None)
    loci.columns = ["chr", "start", "end", "peak_name"]

    # Extract sequences
    X = extract_loci(loci, str(fasta_file), in_window=window).float()

    # Run FIMO
    hits_list = []
    for i in range(int(len(pwms_sub) / batch_size_Fimo_scan)):
        # Split the pwms_sub dictionary into smaller chunks
        start = i * batch_size_Fimo_scan
        end = (i + 1) * batch_size_Fimo_scan
        pwms_sub_chunk = dict(list(pwms_sub.items())[start:end])
        # # Run FIMO on the chunk
        fimo_scores = fimo(pwms_sub_chunk, X, threshold=threshold)
        hits_list.extend(fimo_scores)

    # Handle the last chunk separately
    if len(pwms_sub) % batch_size_Fimo_scan != 0:
        start = (len(pwms_sub) // batch_size_Fimo_scan) * batch_size_Fimo_scan
        pwms_sub_chunk = dict(list(pwms_sub.items())[start:])
        # # Run FIMO on the chunk
        fimo_scores = fimo(pwms_sub_chunk, X, threshold=threshold)
        hits_list.extend(fimo_scores)

    all_tf_cols = sorted(list(set(key_to_tf.values())))

    peak_motif_scores = []

    for k in tqdm(range(len(hits_list))):
        # Group by motif_name and sequence_name, keeping the max score per group
        motif_df = (
            hits_list[k][["motif_name", "sequence_name", "score"]]
            .groupby(["motif_name", "sequence_name"])
            .max()
            .reset_index()
        )

        if motif_df.shape[0] > 0:  # Proceed if there are valid scores
            all_sequences = pd.DataFrame({"sequence_name": range(n_peaks)})

            motif_name = motif_df.motif_name.values[0]
            tf_name = key_to_tf[motif_name]

            # Merge all sequences with motif_df, filling missing values
            complete_df = all_sequences.merge(motif_df, on="sequence_name", how="left")
            complete_df["score"] = complete_df["score"].fillna(
                0
            )  # Fill NaN scores with 0

            # Ensure only the "score" column remains before renaming
            complete_df = complete_df[["sequence_name", "score"]].set_index(
                "sequence_name"
            )
            complete_df.columns = [tf_name]  # Rename the "score" column to the TF name

            # Append to the list
            peak_motif_scores.append(complete_df)

    # Concatenate all the individual dataframes into a single dataframe
    if len(peak_motif_scores) > 0:
        peak_motif_scores = pd.concat(peak_motif_scores, axis=1)
    else:
        logger.warning("No motif scores were computed. Returning an empty DataFrame.")
        peak_motif_scores = pd.DataFrame(index=range(n_peaks))

    # Handle remaining TFs not present in the scores
    remaining_tfs = set(key_to_tf.values()) - set(peak_motif_scores.columns)
    for tf in remaining_tfs:
        peak_motif_scores[tf] = 0

    # Reorder columns to match the final TF list

    final_tf_list = sorted(list(set(key_to_tf.values())))
    peak_motif_scores = peak_motif_scores[final_tf_list]

    scaler = MinMaxScaler()
    motif_scores = scaler.fit_transform(peak_motif_scores.values)

    bed_file_peak = pd.read_csv(bed_file, sep="\t", header=None)
    df_motif = pd.DataFrame(
        motif_scores, columns=peak_motif_scores.columns, index=bed_file_peak[3].values
    )

    logger.info(f"Finished computing motif scores: {df_motif.shape}")
    return df_motif


@beartype
def compute_in_silico_chipseq(
    df_motif: pd.DataFrame,
    atac_matrix: np.ndarray,
    rna_matrix: np.ndarray,
    correlation_percentile: float,
    n_bg_peaks_for_corr: int,
) -> pd.DataFrame:
    """Compute in-silico ChIP-seq signals from motif scores and expression data.

    Integrates motif scores, chromatin accessibility (ATAC), and gene expression (RNA)
    data to predict transcription factor binding, producing in-silico ChIP-seq signals.
    The method computes correlations between peak accessibility and TF expression,
    then combines these with motif scores to generate a comprehensive binding prediction.

    Args:
        df_motif: DataFrame with shape (n_peaks, n_tfs) containing motif scores,
            with peak names as index and TF names as columns.
        atac_matrix: Matrix with shape (n_metacells, n_peaks) containing
            chromatin accessibility data.
        rna_matrix: Matrix with shape (n_metacells, n_tfs) containing
            gene expression data for transcription factors.
        correlation_percentile: Percentile threshold for determining significant
            correlations (higher = more stringent).
        n_bg_peaks_for_corr: Number of background peaks to use per motif for
            establishing correlation significance thresholds.

    Returns:
        DataFrame in long format with columns "peak_name", "Motif_name", and
        "Matching_Score". Scores are scaled to range [-1, 1], where positive values
        indicate activating interactions and negative values indicate repressing
        interactions. Only non-zero scores are included.
    """
    from sklearn.preprocessing import MinMaxScaler
    from tqdm import tqdm

    logger.info("Computing in-silico ChIP-seq correlation...")

    n_cells, n_peaks = atac_matrix.shape
    _, n_tfs = rna_matrix.shape
    if df_motif.shape != (n_peaks, n_tfs):
        logger.warning("df_motif dimension does not match (n_peaks x n_tfs).")

    # Z-score peaks & TF expression
    X = (atac_matrix - atac_matrix.mean(axis=0)) / (atac_matrix.std(axis=0) + 1e-8)
    Y = (rna_matrix - rna_matrix.mean(axis=0)) / (rna_matrix.std(axis=0) + 1e-8)

    # Pearson correlation => (n_peaks x n_tfs)
    pearson_r = (X.T @ Y) / n_cells
    pearson_r = np.nan_to_num(pearson_r)

    pearson_r_act = np.clip(pearson_r, 0, None)  # only positive
    pearson_r_rep = np.clip(pearson_r, None, 0)  # only negative

    pearson_r_act_sig = np.zeros_like(pearson_r_act)
    pearson_r_rep_sig = np.zeros_like(pearson_r_rep)

    tf_list = df_motif.columns

    # Thresholding
    for t in tqdm(range(n_tfs), desc="Thresholding correlation"):
        tf_name = tf_list[t]
        # Find background peaks with smallest motif
        scores_t = df_motif[tf_name].values
        order = np.argsort(scores_t)
        bg_idx = order[
            : min(n_bg_peaks_for_corr, n_peaks)
        ]  # top n_bg smallest motif peaks
        # Activator significance
        bg_vals_act = pearson_r_act[bg_idx, t]
        cutoff_act = np.percentile(bg_vals_act, correlation_percentile)
        # Repressor significance
        bg_vals_rep = pearson_r_rep[bg_idx, t]
        cutoff_rep = np.percentile(bg_vals_rep, 100 - correlation_percentile)

        act_vec = pearson_r_act[:, t]
        rep_vec = pearson_r_rep[:, t]
        pearson_r_act_sig[:, t] = np.where(act_vec > cutoff_act, act_vec, 0)
        pearson_r_rep_sig[:, t] = np.where(rep_vec < cutoff_rep, rep_vec, 0)

    # Combine with motif
    insilico_chipseq_act_sig = df_motif.values * pearson_r_act_sig
    insilico_chipseq_rep_sig = df_motif.values * pearson_r_rep_sig
    insilico_chipseq_sig_all = insilico_chipseq_act_sig + insilico_chipseq_rep_sig

    logger.info("Finished in-silico ChIP-seq computation.")

    peak_index_list = list(df_motif.index)
    insilico_chipseq_sig_all = pd.DataFrame(insilico_chipseq_sig_all)

    insilico_chipseq_sig_all["peak_name"] = peak_index_list
    insilico_chipseq_sig_all = insilico_chipseq_sig_all.set_index("peak_name")
    insilico_chipseq_sig_all.columns = df_motif.columns

    insilico_chipseq_sig_all = insilico_chipseq_sig_all.reset_index().melt(
        id_vars="peak_name", var_name="column", value_name="value"
    )
    insilico_chipseq_sig_all = insilico_chipseq_sig_all[
        insilico_chipseq_sig_all["value"] != 0
    ]

    insilico_chipseq_sig_all.rename(
        columns={"column": "Motif_name", "value": "Matching_Score"}, inplace=True
    )

    scaler = MinMaxScaler(feature_range=(-1, 1))
    insilico_chipseq_sig_scaled = scaler.fit_transform(
        insilico_chipseq_sig_all[["Matching_Score"]]
    )
    insilico_chipseq_sig_all["Matching_Score"] = insilico_chipseq_sig_scaled
    return insilico_chipseq_sig_all
