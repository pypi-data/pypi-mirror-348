"""Functions for filtering genomics data.

This module contains functions for filtering genes, regions, and motif scores
in genomic datasets, particularly for single-cell RNA-seq and ATAC-seq data.
"""

import logging
import subprocess
from pathlib import Path
from typing import List, Optional, Set, Tuple, Union

import numpy as np
import pandas as pd
import scanpy as sc
import scipy.sparse as sp
from anndata import AnnData
from beartype import beartype

from stormi.preprocessing._file_utils import check_command_availability

logger = logging.getLogger(__name__)


@beartype
def filter_genes(
    adata: AnnData,
    protein_coding_only: bool = True,
    filter_mt_genes: bool = True,
    hvg_flavor: str = "highly_variable",
    hvg_fraction: float = 0.1,
    hvg_key: Optional[str] = None,
) -> AnnData:
    """Filter genes in an AnnData object.

    Args:
        adata: AnnData object with genes as columns.
        protein_coding_only: Whether to keep only protein-coding genes. Default is True.
        filter_mt_genes: Whether to filter out mitochondrial genes. Default is True.
        hvg_flavor: Method for highly variable gene selection, one of "highly_variable"
            or "TF_HVG". Default is "highly_variable".
        hvg_fraction: Fraction of genes to select as highly variable. Default is 0.1.
        hvg_key: Key in adata.var to store HVG boolean. Default is None (inferred).

    Returns:
        Filtered AnnData object.
    """
    # Make a copy to avoid modifying the original
    adata_filtered = adata.copy()
    initial_genes = adata_filtered.shape[1]

    # Filter protein-coding genes if requested
    if protein_coding_only and "gene_type" in adata_filtered.var:
        mask_pc = adata_filtered.var["gene_type"] == "protein_coding"
        adata_filtered = adata_filtered[:, mask_pc]
        logger.info(
            f"Filtered protein-coding genes: {adata_filtered.shape[1]} / {initial_genes} "
            f"({adata_filtered.shape[1] / initial_genes:.2%})"
        )

    # Filter mitochondrial genes if requested
    if filter_mt_genes:
        mask_mt = ~adata_filtered.var_names.str.startswith(("MT-", "mt-"))
        adata_filtered = adata_filtered[:, mask_mt]
        logger.info(
            f"Filtered mitochondrial genes: {adata_filtered.shape[1]} / {initial_genes} "
            f"({adata_filtered.shape[1] / initial_genes:.2%})"
        )

    # Select highly variable genes based on the chosen method
    if hvg_flavor == "highly_variable":
        if hvg_key is None:
            hvg_key = "highly_variable"

        # Calculate highly variable genes if not already done
        if hvg_key not in adata_filtered.var:
            try:
                from scanpy.preprocessing import highly_variable_genes

                highly_variable_genes(
                    adata_filtered,
                    n_top_genes=int(adata_filtered.shape[1] * hvg_fraction),
                )
            except ImportError:
                logger.warning(
                    "Scanpy not available for HVG calculation. "
                    "Consider pre-calculating HVGs or installing scanpy."
                )
                # Fallback: select genes with highest variance
                gene_var = (
                    np.array(adata_filtered.X.mean(axis=0)).flatten()
                    if sp.issparse(adata_filtered.X)
                    else adata_filtered.X.mean(axis=0)
                )
                hvg_mask = np.zeros(adata_filtered.shape[1], dtype=bool)
                hvg_mask[
                    np.argsort(-gene_var)[: int(adata_filtered.shape[1] * hvg_fraction)]
                ] = True
                adata_filtered.var[hvg_key] = hvg_mask

        # Filter to HVGs
        adata_filtered = adata_filtered[:, adata_filtered.var[hvg_key]]
        logger.info(
            f"Selected {adata_filtered.shape[1]} / {initial_genes} highly variable genes "
            f"({adata_filtered.shape[1] / initial_genes:.2%})"
        )

    elif hvg_flavor == "TF_HVG":
        # Try to get the list of transcription factors
        try:
            from stormi.db import get_tfs_for_species

            tfs = get_tfs_for_species(
                "human"
                if any(g.startswith("ENSG") for g in adata_filtered.var_names)
                else "mouse"
            )

            # Find TFs that are in our dataset
            tf_mask = adata_filtered.var_names.isin(tfs)
            n_tfs = tf_mask.sum()

            if n_tfs > 0:
                logger.info(f"Found {n_tfs} transcription factors in dataset")

                # For non-TFs, select the top variable genes
                non_tf_adata = adata_filtered[:, ~tf_mask]

                # Calculate variance for non-TF genes
                if sp.issparse(non_tf_adata.X):
                    var = (
                        np.array(non_tf_adata.X.power(2).mean(axis=0)).flatten()
                        - np.array(non_tf_adata.X.mean(axis=0)).flatten() ** 2
                    )
                else:
                    var = non_tf_adata.X.var(axis=0)

                # Select top variable non-TF genes
                n_hvg = int(adata_filtered.shape[1] * hvg_fraction) - n_tfs
                top_var_idx = np.argsort(-var)[:n_hvg]

                # Create mask for selected non-TF genes
                selected_genes_mask = np.zeros(non_tf_adata.shape[1], dtype=bool)
                selected_genes_mask[top_var_idx] = True

                # Combine TF and selected non-TF genes
                final_mask = np.zeros(adata_filtered.shape[1], dtype=bool)
                final_mask[np.where(tf_mask)[0]] = True
                final_mask[np.where(~tf_mask)[0][top_var_idx]] = True

                # Apply the mask
                adata_filtered = adata_filtered[:, final_mask]

                logger.info(
                    f"Selected {adata_filtered.shape[1]} genes: {n_tfs} TFs + {n_hvg} HVGs "
                    f"({adata_filtered.shape[1] / initial_genes:.2%} of initial genes)"
                )
            else:
                logger.warning(
                    "No transcription factors found. Falling back to standard HVG selection."
                )
                # Fallback to standard HVG
                return filter_genes(
                    adata,
                    protein_coding_only=protein_coding_only,
                    filter_mt_genes=filter_mt_genes,
                    hvg_flavor="highly_variable",
                    hvg_fraction=hvg_fraction,
                )
        except ImportError:
            logger.warning(
                "Required dependencies for TF_HVG not available. "
                "Falling back to standard HVG selection."
            )
            # Fallback to standard HVG
            return filter_genes(
                adata,
                protein_coding_only=protein_coding_only,
                filter_mt_genes=filter_mt_genes,
                hvg_flavor="highly_variable",
                hvg_fraction=hvg_fraction,
            )

    return adata_filtered


@beartype
def filter_regions(
    adata: AnnData,
    min_cells: int = 10,
    score_percentile: float = 90,
    score_mode: str = "score",
    promoter_only: bool = False,
) -> AnnData:
    """Filter genomic regions (peaks) in an AnnData object.

    Args:
        adata: AnnData object with regions/peaks as columns.
        min_cells: Minimum number of cells a peak must be detected in.
            Default is 10.
        score_percentile: Percentile threshold for peak scores. Default is 90.
        score_mode: How to calculate peak scores, one of "score" or "std".
            Default is "score".
        promoter_only: Whether to keep only promoter regions. Default is False.

    Returns:
        Filtered AnnData object.
    """
    # Make a copy to avoid modifying the original
    adata_filtered = adata.copy()
    initial_regions = adata_filtered.shape[1]

    # Filter by min cells
    if min_cells > 0:
        if sp.issparse(adata_filtered.X):
            cell_counts = np.array((adata_filtered.X > 0).sum(axis=0)).flatten()
        else:
            cell_counts = np.sum(adata_filtered.X > 0, axis=0)

        mask = cell_counts >= min_cells
        adata_filtered = adata_filtered[:, mask]

        logger.info(
            f"Filtered regions by min cells ({min_cells}): {adata_filtered.shape[1]} / {initial_regions} "
            f"({adata_filtered.shape[1] / initial_regions:.2%})"
        )

    # Filter by score percentile
    if score_percentile > 0:
        if score_mode == "score":
            # Use mean signal as score
            if sp.issparse(adata_filtered.X):
                scores = np.array(adata_filtered.X.mean(axis=0)).flatten()
            else:
                scores = adata_filtered.X.mean(axis=0)
        elif score_mode == "std":
            # Use signal standard deviation as score
            if sp.issparse(adata_filtered.X):
                mean = np.array(adata_filtered.X.mean(axis=0)).flatten()
                mean_sq = np.array(adata_filtered.X.power(2).mean(axis=0)).flatten()
                scores = np.sqrt(mean_sq - mean**2)
            else:
                scores = adata_filtered.X.std(axis=0)
        else:
            raise ValueError(f"Unknown score_mode: {score_mode}")

        # Calculate threshold and apply filter
        threshold = np.percentile(scores, score_percentile)
        mask = scores >= threshold
        adata_filtered = adata_filtered[:, mask]

        logger.info(
            f"Filtered regions by {score_mode} score (percentile {score_percentile}): "
            f"{adata_filtered.shape[1]} / {initial_regions} "
            f"({adata_filtered.shape[1] / initial_regions:.2%})"
        )

    # Filter for promoter regions if requested
    if promoter_only and "region_type" in adata_filtered.var:
        mask = adata_filtered.var["region_type"] == "promoter"
        adata_filtered = adata_filtered[:, mask]

        logger.info(
            f"Filtered for promoter regions: {adata_filtered.shape[1]} / {initial_regions} "
            f"({adata_filtered.shape[1] / initial_regions:.2%})"
        )

    return adata_filtered


@beartype
def filter_motif_scores(
    motif_scores: pd.DataFrame,
    adata_rna: AnnData,
    adata_atac: AnnData,
) -> pd.DataFrame:
    """Filter motif scores to include only genes and peaks in filtered datasets.

    Args:
        motif_scores: DataFrame with motif scores.
        adata_rna: AnnData object with filtered RNA data.
        adata_atac: AnnData object with filtered ATAC data.

    Returns:
        Filtered motif scores DataFrame.
    """
    # Extract TF names from gene index
    motif_tfs = motif_scores.index.unique().tolist()

    # Filter to TFs present in RNA data
    common_tfs = [tf for tf in motif_tfs if tf in adata_rna.var_names]
    logger.info(f"Found {len(common_tfs)} / {len(motif_tfs)} TFs in RNA data")

    # Filter motif scores to only include TFs in RNA data
    filtered_scores = motif_scores.loc[common_tfs]

    # Filter to peaks present in ATAC data
    peak_cols = [col for col in filtered_scores.columns if col in adata_atac.var_names]
    logger.info(
        f"Found {len(peak_cols)} / {len(filtered_scores.columns)} peaks in ATAC data"
    )

    # Filter motif scores to only include peaks in ATAC data
    filtered_scores = filtered_scores[peak_cols]

    logger.info(
        f"Filtered motif scores: {filtered_scores.shape[0]} TFs x {filtered_scores.shape[1]} peaks"
    )

    return filtered_scores


@beartype
def func_mitochondrial_genes(data_rna: AnnData) -> AnnData:
    """Remove mitochondrial genes (with 'mt-' prefix) from RNA data.

    Args:
        data_rna: AnnData object containing RNA data.

    Returns:
        AnnData with mitochondrial genes removed.
    """
    orig_num_genes = data_rna.shape[1]
    data_rna.var["mt"] = [gene.lower().startswith("mt-") for gene in data_rna.var_names]
    keep_mask = ~data_rna.var["mt"]
    data_rna = data_rna[:, keep_mask].copy()
    dropped = orig_num_genes - data_rna.shape[1]

    logger.info(f"Removed {dropped} mitochondrial genes with prefix= mt-")
    return data_rna


@beartype
def func_protein_coding_genes(data_rna: AnnData, gtf_df: pd.DataFrame) -> AnnData:
    """Remove non-protein coding genes based on annotation.

    Args:
        data_rna: AnnData object containing RNA data.
        gtf_df: DataFrame containing gene annotations from GTF file.

    Returns:
        AnnData with only protein-coding genes.
    """
    # Remove non-protein coding genes based on annotation
    df_protein_coding = gtf_df[gtf_df["gene_type"] == "protein_coding"]
    pc_genes = set(df_protein_coding["gene_name"].unique())
    rna_genes = set(data_rna.var_names)
    keep_genes = sorted(list(pc_genes & rna_genes))
    data_rna = data_rna[:, keep_genes].copy()
    logger.info(f"Filtered to protein-coding genes: {data_rna.shape[1]} genes left.")
    return data_rna


@beartype
def TF_HVG_selection(
    data_rna: AnnData,
    motif_dir: Path,
    num_genes_hvg: int,
    num_tfs_hvg: int,
    species: str,
    motif_database: str,
) -> Tuple[AnnData, List[str], List[str]]:
    """Select highly variable genes (HVGs) and transcription factors (TFs).

    Args:
        data_rna: AnnData object containing RNA data.
        motif_dir: Directory containing motif files.
        num_genes_hvg: Number of HV non-TF genes to select.
        num_tfs_hvg: Number of HV TF genes to select.
        species: Species name (e.g., "mouse", "human").
        motif_database: Name of the motif database (e.g., "cisbp").

    Returns:
        Tuple containing:
        - Filtered AnnData object
        - List of selected non-TF genes
        - List of selected TF genes
    """
    logger.info("Selecting HVGs and TFs...")

    # Load all possible TFs
    motif_path = motif_dir / f"{motif_database}_{species}.meme"
    tf_names_all = []
    with open(motif_path, "r") as f:
        for line in f:
            if line.startswith("MOTIF"):
                parts = line.strip().split()
                if len(parts) >= 3:
                    tf_name = parts[2].split("_")[0].strip("()").strip()
                    tf_names_all.append(tf_name)
    tf_names_all = sorted(list(set(tf_names_all)))

    # Computing HVG among TFs
    tf_candidates = sorted(list(set(tf_names_all) & set(data_rna.var_names)))
    data_rna_tf = data_rna[:, tf_candidates].copy()

    sc.pp.normalize_total(data_rna_tf)
    sc.pp.log1p(data_rna_tf)
    sc.pp.highly_variable_genes(data_rna_tf, n_top_genes=num_tfs_hvg, subset=True)

    selected_tfs = sorted(list(data_rna_tf.var_names))

    # Computing HVG among non-TFs
    non_tf_candidates = set(data_rna.var_names) - set(tf_candidates)
    data_rna_non_tf = data_rna[:, sorted(list(non_tf_candidates))].copy()

    sc.pp.normalize_total(data_rna_non_tf)
    sc.pp.log1p(data_rna_non_tf)
    sc.pp.highly_variable_genes(data_rna_non_tf, n_top_genes=num_genes_hvg, subset=True)

    selected_non_tfs = sorted(list(data_rna_non_tf.var_names))

    final_genes = selected_non_tfs
    final_tfs = selected_tfs

    combined = final_genes + final_tfs
    data_rna = data_rna[:, combined].copy()

    # Mark gene_type in .var
    gene_types = ["HVG"] * len(final_genes) + ["TF"] * len(final_tfs)
    data_rna.var["gene_type"] = gene_types

    logger.info(
        f"Selected {len(final_genes)} HVGs from {len(non_tf_candidates)} available HVGs + "
        f"{len(final_tfs)} TFs from {len(tf_candidates)} available TFs."
    )
    return data_rna, final_genes, final_tfs


@beartype
def select_highly_variable_peaks_by_std(
    data_atac: AnnData, n_top_peaks: int, cluster_key: str
) -> AnnData:
    """Select highly variable peaks using cluster-based standard deviation.

    Args:
        data_atac: AnnData object containing ATAC data.
        n_top_peaks: Number of top peaks to select.
        cluster_key: Key in data_atac.obs for cluster assignments.

    Returns:
        AnnData object with selected peaks.
    """
    if cluster_key not in data_atac.obs.columns:
        logger.warning(
            f"{cluster_key} not found in data_atac.obs; skipping peak selection."
        )
        return data_atac

    clusters = data_atac.obs[cluster_key].unique()
    cluster_groups = data_atac.obs.groupby(cluster_key)
    mean_list = []

    for c_label in clusters:
        idx_cells = cluster_groups.get_group(c_label).index
        mat = data_atac[idx_cells].X
        if sp.issparse(mat):
            # Convert to dense
            mat = mat.toarray()
        mat = (mat + 1) // 2  # get fragments
        mean_vec = mat.mean(axis=0).A1 if hasattr(mat, "A1") else mat.mean(axis=0)
        mean_list.append(mean_vec)

    cluster_matrix = np.vstack(mean_list)  # shape=(n_clusters, n_peaks)
    stdev_peaks = cluster_matrix.std(axis=0)
    data_atac.var["std_cluster"] = stdev_peaks

    if n_top_peaks < data_atac.shape[1]:
        sorted_idx = np.argsort(stdev_peaks)[::-1]
        keep_idx = sorted_idx[:n_top_peaks]
        mask = np.zeros(data_atac.shape[1], dtype=bool)
        mask[keep_idx] = True
        data_atac_sub = data_atac[:, mask].copy()
        logger.info(
            f"Selected top {n_top_peaks} variable peaks (by std across {cluster_key})."
        )
        return data_atac_sub
    else:
        logger.info("n_top_peaks >= total peaks; no filtering applied.")
        return data_atac


@beartype
def keep_promoters_and_select_hv_peaks(
    data_atac: AnnData, total_n_peaks: int, cluster_key: str, promoter_col: str
) -> AnnData:
    """Keep all promoter peaks and select highly variable non-promoter peaks.

    1) Identifies all promoter peaks where var[promoter_col] == True
    2) Keeps all promoters
    3) For non-promoter peaks, selects the top (total_n_peaks - #promoters) by std
    4) Final set = all promoters + HV among non-promoters

    Args:
        data_atac: AnnData object containing ATAC data.
        total_n_peaks: Target number of peaks to select.
        cluster_key: Key in data_atac.obs for cluster assignments.
        promoter_col: Column in data_atac.var indicating if a peak is a promoter.

    Returns:
        AnnData object with selected peaks.
    """
    if promoter_col not in data_atac.var.columns:
        logger.warning(
            f"Column {promoter_col} not found in data_atac.var; no special promoter logic."
        )
        # fallback: just do normal HV selection
        return select_highly_variable_peaks_by_std(
            data_atac, total_n_peaks, cluster_key
        )
    else:
        # (A) Extract promoter vs non-promoter
        promoter_mask = data_atac.var[promoter_col].values == True
        promoter_peaks = data_atac.var_names[promoter_mask]
        n_promoters = len(promoter_peaks)

        logger.info(
            f"Found {n_promoters} promoter peaks. Target total is {total_n_peaks}."
        )

        if n_promoters >= total_n_peaks:
            # Just keep all promoters, ignoring user target or raise warning
            logger.warning(
                f"Promoter peaks ({n_promoters}) exceed num_peaks={total_n_peaks}. "
                "Keeping all promoters, final set might exceed user target."
            )
            data_atac_sub = data_atac[:, promoter_peaks].copy()
            return data_atac_sub
        else:
            # (B) We keep all promoters, and we can select HV among the non-promoter peaks
            n_needed = total_n_peaks - n_promoters
            logger.info(
                f"Selecting HV among non-promoters => picking {n_needed} peaks."
            )

            # Subset to non-promoters
            non_promoter_mask = ~promoter_mask
            data_atac_nonprom = data_atac[:, non_promoter_mask].copy()

            # HV selection among non-promoters for n_needed
            data_atac_nonprom_hv = select_highly_variable_peaks_by_std(
                data_atac_nonprom, n_needed, cluster_key
            )

            # Final union => promoter peaks + HV(non-promoters)
            final_promoter_set = set(promoter_peaks)
            final_nonprom_set = set(data_atac_nonprom_hv.var_names)
            final_set = list(final_promoter_set.union(final_nonprom_set))

            data_atac_sub = data_atac[:, final_set].copy()
            logger.info(
                f"Final set => {len(promoter_peaks)} promoter + "
                f"{data_atac_nonprom_hv.shape[1]} HV => total {data_atac_sub.shape[1]} peaks."
            )
            return data_atac_sub


@beartype
def bed_file_intersection(
    genome_dir: Path,
    output_dir: Path,
    data_atac: AnnData,
    genome_assembly: str,
    species: str,
    window_size: int,
    gtf_df: pd.DataFrame,
    final_genes: List[str],
    final_tfs: List[str],
) -> AnnData:
    """Intersect ATAC peaks with gene windows from GTF.

    Creates BED files for peaks and gene windows, then uses bedtools or a Python fallback
    to find overlaps.

    Args:
        genome_dir: Directory containing genome files.
        output_dir: Directory to save output files.
        data_atac: AnnData object containing ATAC data.
        genome_assembly: Genome assembly name (e.g., "mm10", "hg38").
        species: Species name (e.g., "mouse", "human").
        window_size: Window size around genes for intersection.
        gtf_df: DataFrame containing gene annotations from GTF file.
        final_genes: List of selected genes.
        final_tfs: List of selected TFs.

    Returns:
        AnnData object with peaks that overlap gene windows.
    """
    create_dir_if_not_exists(output_dir)

    # 1) Create a BED file with all peaks
    data_atac.var["chr"] = [v.split(":")[0] for v in data_atac.var_names]
    data_atac.var["start"] = [
        int(v.split(":")[1].split("-")[0]) for v in data_atac.var_names
    ]
    data_atac.var["end"] = [
        int(v.split(":")[1].split("-")[1]) for v in data_atac.var_names
    ]
    data_atac.var["peak_name"] = data_atac.var_names

    all_peaks_bed = output_dir / "peaks_all.bed"
    data_atac.var[["chr", "start", "end", "peak_name"]].to_csv(
        all_peaks_bed, sep="\t", header=False, index=False
    )

    # 2) Create a BED file with all genes + TFs
    # We're going to create gene windows based on GTF
    logger.info(f"Creating gene windows with {window_size} bp around genes...")
    final_genes_tfs = final_genes + final_tfs
    gene_mask = gtf_df["gene_name"].isin(final_genes_tfs)
    gene_gtf = gtf_df[gene_mask].copy()
    logger.info(f"Found {gene_mask.sum()} entries for selected genes in GTF.")

    # For the genes in our list, extend +/- window_size
    gene_bed = output_dir / "genes_window.bed"
    extended_genes = []
    for _, gene_row in gene_gtf.iterrows():
        chrom = gene_row["seqname"]
        start = max(0, gene_row["start"] - window_size)
        end = gene_row["end"] + window_size
        name = gene_row["gene_name"]
        strand = gene_row["strand"]
        extended_genes.append([chrom, start, end, name, strand])

    gene_df = pd.DataFrame(
        extended_genes, columns=["chr", "start", "end", "gene_name", "strand"]
    )
    gene_df.to_csv(gene_bed, sep="\t", header=False, index=False)

    # 3) Run bedtools intersect or fallback to Python
    intersected_bed = output_dir / "peaks_intersected.bed"

    if check_command_availability("bedtools"):
        cmd = f"bedtools intersect -u -wa -a {all_peaks_bed} -b {gene_bed} > {intersected_bed}"
        logger.info(f"Running: {cmd}")

        try:
            subprocess.run(cmd, shell=True, check=True)

            peaks_intersected = pd.read_csv(intersected_bed, sep="\t", header=None)
            peaks_intersected.columns = ["chr", "start", "end", "peak_name"]
            windowed_set = set(peaks_intersected["peak_name"])

        except subprocess.CalledProcessError:
            logger.warning(
                "Error running bedtools. Using fallback method for intersection."
            )
            windowed_set = simple_bed_intersection(all_peaks_bed, gene_bed)
    else:
        logger.warning(
            "bedtools command not found in PATH. Using fallback Python-based intersection method. "
            "For better performance, please install bedtools (https://bedtools.readthedocs.io/)."
        )
        windowed_set = simple_bed_intersection(all_peaks_bed, gene_bed)

    # Subset data_atac to these peaks
    data_atac = data_atac[:, list(windowed_set)].copy()
    logger.info(f"After gene-window filtering => shape={data_atac.shape}")
    return data_atac


@beartype
def simple_bed_intersection(peaks_bed: Path, genes_bed: Path) -> Set[str]:
    """Simple Python-based implementation of bedtools intersect.

    This is a fallback for when bedtools is not available.

    Args:
        peaks_bed: Path to BED file containing peaks.
        genes_bed: Path to BED file containing extended gene regions.

    Returns:
        Set of peak names that overlap with any gene region.
    """
    logger.info("Using Python-based intersection as fallback for bedtools")

    peaks = pd.read_csv(peaks_bed, sep="\t", header=None)
    peaks.columns = ["chr", "start", "end", "peak_name"]

    genes = pd.read_csv(genes_bed, sep="\t", header=None)
    genes.columns = ["chr", "start", "end", "gene_name", "strand"]

    peaks_by_chr = {chr_name: group for chr_name, group in peaks.groupby("chr")}
    genes_by_chr = {chr_name: group for chr_name, group in genes.groupby("chr")}

    overlapping_peaks = set()

    for chr_name, chr_peaks in peaks_by_chr.items():
        if chr_name not in genes_by_chr:
            continue

        chr_genes = genes_by_chr[chr_name]

        for _, peak in chr_peaks.iterrows():
            peak_start = peak["start"]
            peak_end = peak["end"]

            for _, gene in chr_genes.iterrows():
                gene_start = gene["start"]
                gene_end = gene["end"]

                if not (peak_end <= gene_start or peak_start >= gene_end):
                    overlapping_peaks.add(peak["peak_name"])
                    break

    overlapping_peaks_df = peaks[peaks["peak_name"].isin(overlapping_peaks)]
    intersected_bed = peaks_bed.parent / "peaks_intersected.bed"
    overlapping_peaks_df.to_csv(intersected_bed, sep="\t", header=False, index=False)

    logger.info(
        f"Found {len(overlapping_peaks)} peaks overlapping with extended gene regions"
    )
    return overlapping_peaks


def create_dir_if_not_exists(directory: Path) -> None:
    """Create the directory if it does not exist.

    Args:
        directory: Path to directory to create.
    """
    if not directory.exists():
        logger.info(f"Creating directory: {directory}")
        directory.mkdir(parents=True, exist_ok=True)
