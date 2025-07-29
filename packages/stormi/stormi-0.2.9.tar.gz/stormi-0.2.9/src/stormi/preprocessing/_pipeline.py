"""Functions for constructing preprocessing pipelines for genomics data.

This module contains functions for building preprocessing pipelines that combine
multiple processing steps for single-cell genomics data, particularly for
RNA-seq and ATAC-seq data integration.
"""

import logging
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import torch
from anndata import AnnData
from beartype import beartype

from stormi.preprocessing._motifs import compute_in_silico_chipseq, compute_motif_scores

logger = logging.getLogger(__name__)


@beartype
def preprocessing_pipeline(
    main_dir: Path,
    data_rna: AnnData,
    data_atac: AnnData,
    drop_mitochondrial_genes: bool = True,
    drop_non_protein_coding_genes: bool = True,
    HVG_Genes_TF: bool = True,
    gene_bed_intersection: bool = True,
    perform_clustering: bool = True,
    peak_selection: bool = True,
    motif_analysis: bool = True,
    chipseq_analysis: bool = True,
    species: str = "mouse",
    motif_database: str = "cisbp",
    genome_assembly: str = "mm10",
    num_tfs_hvg: int = 300,
    num_genes_hvg: int = 3000,
    window_size: int = 500000,
    resolution: int = 5,
    grouping_key: str = "leiden",
    batch_key: str = "sample",
    num_peaks: int = 50000,
    cluster_key: str = "leiden",
    promoter_col: str = "is_promoter",
    motif_match_pvalue_threshold: float = 1e-3,
    batch_size_Fimo_scan: int = 100,
    window: int = 500,
    correlation_percentile: float = 95.0,
    n_bg_peaks_for_corr: int = 5000,
    batch_size_insilico_chipseq: int = 10,
) -> Optional[pd.DataFrame]:
    """
    Preprocessing Pipeline from Manu  Saraswat

    Args:
        main_dir (Path):
            Path to the main directory containing the input files and where other files will be stored/downloaded.
        data_rna (AnnData):
            Annotated RNA expression matrix containing gene expression data for each cell.
        data_atac (AnnData):
            Annotated ATAC-seq matrix containing chromatin accessibility data for each cell.
        drop_mitochondrial_genes (bool): optional
            Preprocessing step to remove all mitochondrial genes from data_rna. Default is True.
        drop_non_protein_coding_genes (bool): optional
            Preprocessing step to remove all non protein coding genes from data_rna. Default is True.
        HVG_Genes_TF (bool): optional
            Preprocessing step to select highly variable TF genes and HVG non TF genes. Default is True.
        gene_bed_intersection (bool): optional
            Preprocessing step to intersect Peaks with Genes. Default is True.
        perform_clustering (bool): optional
            Preprocessing step to perform temporary clustering on data_rna/_atac. Default is True.
        peak_selection (bool): optional
            Preprocessing step to slect TF peaks and HV Peaks across clustering. Default is True.
        motif_analysis (bool): optional
            Motif Matching can be turned off if one wants only the filter RNA/ATAC data. Default is True.
        chipseq_analysis (bool): optional
            Insilico_chiseq can be turned off if one wants only Motif matching without filtering afterwards. Default is True.
        species (str): optional
            The species being analyzed. Default is "mouse".
        motif_database (str): optional
            The database used for transcription factor motif analysis. Default is "cisbp".
        genome_assembly (str): optional
            The genome assembly version to use for the analysis. Default is "mm10".
        num_tfs_hvg (int): optional
            Number of HV TF genes to be selected. Default is 300.
        num_genes_hvg (int): optional
            Number of HV  non TF genes to be selected. Default is 3000.
        window_size (int): optional
            Window size for Gene-Peaks Intersection. Default is 80,000.
        resolution (int): optional
            Resolution parameter for clustering. Default is 5.
        grouping_key (str): optional
            Key used to define groups in the clustering process. Default is "leiden".
        batch_key (str): optional
            Metadata key used for batch correction or grouping cells by batch. Default is "sample".
        num_peaks (int): optional
            The total number of TF Peaks + HV Peaks across clustering to be selected. Default is 50,000.
        cluster_key (str): optional
            Key used to assign cluster labels to cells. Default is "leiden".
        promoter_col (str): optional
            Column name indicating whether a genomic region is a promoter. Default is "is_promoter".
        motif_match_pvalue_threshold (float): optional
            P-value threshold for motif matching algorithm. Default is 1e-3.
        batch_size_Fimo_scan (int): optional
            Number of TF motifs to process in each batch during motif matching. Default is 100.
        window (int): optional
            Size of the window around peak centre for motif scanning. Default is 500.
        correlation_percentile (int): optional
            Percentile threshold for selecting highly correlated features. Default is 95.
        n_bg_peaks_for_corr (int): optional
            Number of background peaks used for correlation analysis. Default is 5000.
        batch_size_insilico_chipseq (int): Optional
            Number of batches in which matrix for compute_insilico_chipseq is split up. Default is 10.


    Returns:
        insilico_chipseq.csv: pd.DataFrame containing filtered motif matches with corresponding gene and region names and motif scores.
    """
    # Import specific functions from the refactored modules
    from gtfparse import read_gtf
    from tangermeme.io import read_meme

    from stormi.preprocessing._file_utils import (
        create_dir_if_not_exists,
    )
    from stormi.preprocessing._filtering import (
        TF_HVG_selection,
        bed_file_intersection,
        func_mitochondrial_genes,
        func_protein_coding_genes,
        keep_promoters_and_select_hv_peaks,
    )
    from stormi.preprocessing._metacells import create_metacells

    # define folder structure
    genome_dir = main_dir / Path("Prepared")
    motif_dir = main_dir / Path("Prepared")
    output_dir = main_dir / Path("Generated")
    create_dir_if_not_exists(output_dir)

    # Intersection: Keeping only cells which are present in both rna and atac files
    common_idx = data_rna.obs_names.intersection(data_atac.obs_names)
    data_rna = data_rna[common_idx].copy()
    data_atac = data_atac[common_idx].copy()
    logger.info(f"Intersected cells: now RNA={data_rna.shape}, ATAC={data_atac.shape}")

    # Mitochondrial Genes: Dropping mitochondrial genes in RNA Data
    if drop_mitochondrial_genes:
        data_rna = func_mitochondrial_genes(data_rna)
    else:
        logger.info("Kept mitochondrial genes")

    # Protein Coding Genes: Dropping non-protein coding genes in RNA Data
    # Load the annotations for genes
    gtf_path = genome_dir / Path(f"{species}_annotation.gtf")
    logger.info(f"Loading GTF from {gtf_path}")
    df = read_gtf(gtf_path)
    gtf_df = pd.DataFrame(df)
    gtf_df.columns = df.columns

    if drop_non_protein_coding_genes:
        data_rna = func_protein_coding_genes(data_rna, gtf_df)
    else:
        logger.info("Kept non-protein coding genes")

    # TF + HVG selection
    if HVG_Genes_TF:
        data_rna, final_genes, final_tfs = TF_HVG_selection(
            data_rna, motif_dir, num_genes_hvg, num_tfs_hvg, species, motif_database
        )
    else:
        # Load all possible TF
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
        final_tfs = sorted(list(set(tf_names_all) & set(data_rna.var_names)))
        final_genes = sorted(list(set(data_rna.var_names) - set(final_tfs)))
        combined = final_genes + final_tfs
        data_rna = data_rna[:, combined].copy()
        gene_types = ["HVG"] * len(final_genes) + ["TF"] * len(final_tfs)
        data_rna.var["gene_type"] = gene_types

        logger.info("No HVG and TF were selected. All were kept.")
        logger.info(
            f"Selected {len(final_genes)} non TF Genes from {len(data_rna.var_names)} available Genes  + {len(final_tfs)} TFs from {len(tf_names_all)} available TFs."
        )

    # Gene Bed Intersection
    if gene_bed_intersection:
        data_atac = bed_file_intersection(
            genome_dir,
            output_dir,
            data_atac,
            genome_assembly,
            species,
            window_size,
            gtf_df,
            final_genes,
            final_tfs,
        )
    else:
        logger.info("No gene-window filtering was done. All peaks were kept.")

    # Temporary Clustering

    # if no batch is defined one can parse on a dummy batch
    # e.g. data_rna.obs["sample"] = ["A"] * data_rna.shape[0]
    if perform_clustering:
        data_rna.obs["sample"] = ["A"] * data_rna.shape[0]
        rna_metacell, atac_metacell = create_metacells(
            data_rna, data_atac, grouping_key, resolution, batch_key
        )
        # Copy Labels
        data_atac.obs["leiden"] = data_rna.obs["leiden"]
    else:
        logger.info("No Clustering was performed")

    # Keep promoter peaks + HV from the rest => total # = num_peaks
    if peak_selection:
        data_atac = keep_promoters_and_select_hv_peaks(
            data_atac=data_atac,
            total_n_peaks=num_peaks,
            cluster_key=cluster_key,
            promoter_col=promoter_col,
        )
        logger.info(f"Final shape after combining promoters + HV => {data_atac.shape}")
    else:
        logger.info("No peak selection was performed")

    # Creating Bed for selected peaks
    data_atac.var["chr"] = [v.split(":")[0] for v in data_atac.var_names]
    data_atac.var["start"] = [
        int(v.split(":")[1].split("-")[0]) for v in data_atac.var_names
    ]
    data_atac.var["end"] = [
        int(v.split(":")[1].split("-")[1]) for v in data_atac.var_names
    ]
    data_atac.var["peak_name"] = data_atac.var_names
    peaks_bed = output_dir / "peaks_selected.bed"
    data_atac.var[["chr", "start", "end", "peak_name"]].to_csv(
        peaks_bed, sep="\t", header=False, index=False
    )

    # Saving Processed Data
    common_cells = data_rna.obs_names.intersection(data_atac.obs_names)
    data_rna = data_rna[common_cells].copy()
    data_atac = data_atac[common_cells].copy()

    # Save
    rna_path = output_dir / Path("rna_processed.h5ad")
    atac_path = output_dir / Path("atac_processed.h5ad")
    data_rna.write_h5ad(rna_path)
    data_atac.write_h5ad(atac_path)
    logger.info(f"Saved processed RNA to {rna_path} with shape={data_rna.shape}")
    logger.info(f"Saved processed ATAC to {atac_path} with shape={data_atac.shape}")

    # Motif Matching
    if motif_analysis:
        # Loading necessary data
        motif_path = motif_dir / f"{motif_database}_{species}.meme"

        # Read .meme motif file
        logger.info(f"Reading motif file: {motif_path}")
        pwms = read_meme(motif_path)

        # Converting PWMs to format of FIMO's input
        keys_list = pwms.keys()
        bg = 0.25
        psd = 0.0001
        for x in keys_list:
            pwms[x] = np.exp(pwms[x]) * bg - psd

        # Subset TF to only TF of interest
        selected_keys = []
        selected_tfs = []
        for key in pwms.keys():
            # Example parse: "MOTIF  something Tbx5_..."
            tf_name = key.split(" ")[1].split("_")[0].strip("()").strip()
            if tf_name in final_tfs:
                selected_keys.append(key)
                selected_tfs.append(tf_name)

        df_map = pd.DataFrame(
            {"key": selected_keys, "TF": selected_tfs}
        ).drop_duplicates("TF")
        pwms_sub = {row.key: pwms[row.key] for _, row in df_map.iterrows()}
        key_to_tf = dict(zip(df_map["key"], df_map["TF"]))

        logger.info(f"Subselected {len(pwms_sub)} motifs for {len(final_tfs)} TFs.")

        df_motif = compute_motif_scores(
            bed_file=output_dir / Path("peaks_selected.bed"),
            fasta_file=genome_dir / f"{species}_{genome_assembly}.fa",
            pwms_sub=pwms_sub,
            key_to_tf=key_to_tf,
            n_peaks=data_atac.shape[1],
            window=window,
            threshold=motif_match_pvalue_threshold,
            batch_size_Fimo_scan=batch_size_Fimo_scan,
        )
    else:
        logger.info(" No motif matching was performed.")
        return
    print(f"shape motif stuff:{df_motif.shape}")

    # Insilico Chipseq
    if chipseq_analysis:
        # Filtering meta cells to new set of peaks
        atac_metacell = atac_metacell[:, data_atac.var_names].copy()
        tf_mask = rna_metacell.var["gene_type"] == "TF"
        rna_matrix = rna_metacell.X[:, tf_mask]  # shape=(n_meta, n_tfs)
        atac_matrix = atac_metacell.X  # shape=(n_meta, n_peaks)

        # Batch input of insilico_chipseq
        batch_rna_matrix = np.array_split(
            rna_matrix, batch_size_insilico_chipseq, axis=1
        )
        batch_df_motif = np.array_split(df_motif, batch_size_insilico_chipseq, axis=1)
        insilico_chipseq = pd.DataFrame(
            columns=["peak_name", "Motif_name", "Matching_Score"]
        )

        for i in range(batch_size_insilico_chipseq):
            intermediate_insilico_chipseq = compute_in_silico_chipseq(
                atac_matrix=atac_matrix,
                rna_matrix=batch_rna_matrix[i],
                df_motif=batch_df_motif[i],
                correlation_percentile=correlation_percentile,
                n_bg_peaks_for_corr=n_bg_peaks_for_corr,
            )
            insilico_chipseq = pd.concat(
                [insilico_chipseq, intermediate_insilico_chipseq],
                axis=0,
                ignore_index=True,
            )

        # Save formatted output
        insilico_chipseq.to_csv(output_dir / "insilico_chipseq.csv")

        return insilico_chipseq
    else:
        logger.info(" No insilico_chipseq was performed.")
        raw_motif_results = df_motif.reset_index().melt(
            id_vars="index", var_name="column", value_name="value"
        )
        raw_motif_results = raw_motif_results[raw_motif_results["value"] != 0]
        raw_motif_results.rename(
            columns={
                "index": "peak_name",
                "column": "Motif_name",
                "value": "Matching_Score",
            },
            inplace=True,
        )
    return raw_motif_results
