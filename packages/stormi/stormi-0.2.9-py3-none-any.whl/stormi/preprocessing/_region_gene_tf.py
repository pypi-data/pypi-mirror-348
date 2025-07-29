"""Functions for analyzing region-gene-TF relationships."""

import jax.numpy as jnp
import numpy as np
import pandas as pd
import pyranges as pr
from anndata import AnnData
from beartype import beartype
from pybiomart import Server


def extract_region_tf_pairs(
    dataframe, adata_atac, adata_rna, region_col="peak_name", tf_col="Motif_name"
):
    """Extract non-zero region-TF pairs.

    Args:
        dataframe: A pandas DataFrame containing region-TF metadata.
        adata_atac: AnnData object for ATAC data (regions/peaks).
        adata_rna: AnnData object for RNA data (genes/TFs).
        region_col: Column name for region (peak) identifiers in the DataFrame.
        tf_col: Column name for TF (gene) names in the DataFrame.

    Returns:
        A JAX numpy array of region-TF pairs.
    """
    # Collect region-TF pairs as tuples
    region_tf_pairs = []
    for _, row in dataframe.iterrows():
        region_name = row[region_col]
        tf_name = row[tf_col]

        # Check existence in AnnData objects
        if region_name in adata_atac.var_names and tf_name in adata_rna.var_names:
            region_idx = adata_atac.var_names.get_loc(region_name)
            tf_idx = adata_rna.var_names.get_loc(tf_name)
            region_tf_pairs.append((region_idx, tf_idx))

    # Convert to jax array
    region_tf_pairs = jnp.array(region_tf_pairs, dtype=np.int32)

    return region_tf_pairs


def build_gene_tss_dict(adata_rna, dataset_name="mmusculus_gene_ensembl"):
    """Query Ensembl BioMart for gene TSS locations.

    Args:
        adata_rna: An AnnData object with gene names in `adata_rna.var_names`.
        dataset_name: BioMart dataset name, typically "mmusculus_gene_ensembl" for mouse.

    Returns:
        A dictionary mapping gene names to (chromosome, TSS position) tuples.
    """
    # 1) Connect to Ensembl via pybiomart
    server = Server(host="http://www.ensembl.org")
    dataset = server.marts["ENSEMBL_MART_ENSEMBL"].datasets[dataset_name]

    # 2) Query for genes
    df = dataset.query(
        attributes=[
            "chromosome_name",  # might return 'Chromosome/scaffold name'
            "start_position",  # might return 'Gene start (bp)'
            "end_position",  # might return 'Gene end (bp)'
            "strand",  # might return 'Strand'
            "external_gene_name",  # might return 'Gene name'
        ]
    )

    rename_dict = {}
    for col in df.columns:
        c_lower = col.lower()
        if "chromosome" in c_lower:
            rename_dict[col] = "chromosome_name"
        elif "start" in c_lower:
            rename_dict[col] = "start_position"
        elif "end" in c_lower:
            rename_dict[col] = "end_position"
        elif "strand" in c_lower:
            rename_dict[col] = "strand"
        elif "gene name" in c_lower or "external_gene_name" in c_lower:
            rename_dict[col] = "external_gene_name"

    df.rename(columns=rename_dict, inplace=True)

    # 4) Convert to a dictionary: gene_name -> (chrom, tss)
    #    TSS depends on the strand
    gene_dict = {}
    rna_gene_set = set(adata_rna.var_names)

    for row in df.itertuples(index=False):
        chrom = str(row.chromosome_name)
        start = int(row.start_position)
        end = int(row.end_position)
        strand = int(row.strand)  # 1 or -1 for Ensembl
        gname = str(row.external_gene_name)

        # Skip if gene not in adata_rna
        if gname not in rna_gene_set:
            continue

        # Optional: skip weird contigs
        if not chrom.isdigit() and chrom not in ["X", "Y"]:
            continue

        # TSS depends on strand
        tss = start if strand == 1 else end

        # If multiple lines appear for the same gene, you can decide how to handle them
        if gname not in gene_dict:
            gene_dict[gname] = (chrom, tss)

    return gene_dict


def parse_region_name(region_str):
    """Parse region name like 'chr1:1000-2000' into chromosome, start, and end.

    Args:
        region_str: String in the format 'chr1:1000-2000'.

    Returns:
        Tuple containing (chromosome, start, end).
    """
    region_str = region_str.replace("chr", "")  # remove "chr" if present
    chrom, coords = region_str.split(":")
    start, end = coords.split("-")
    start, end = int(start), int(end)
    return chrom, start, end


def build_pyranges_for_regions(adata_atac):
    """Convert ATAC regions to PyRanges object.

    Args:
        adata_atac: AnnData object with ATAC data.

    Returns:
        PyRanges object with columns: Chromosome, Start, End, region_idx.
    """
    rows = []
    for region_idx, region_str in enumerate(adata_atac.var_names):
        chrom, start, end = parse_region_name(region_str)
        rows.append([chrom, start, end, region_idx])
    df_regions = pd.DataFrame(
        rows, columns=["Chromosome", "Start", "End", "region_idx"]
    )
    return pr.PyRanges(df_regions)


def build_pyranges_for_genes(adata_rna, gene_dict):
    """Convert gene TSS locations to PyRanges intervals.

    For each gene in adata_rna, if it's in gene_dict, create a PyRanges interval
    at [tss, tss+1].

    Args:
        adata_rna: AnnData object with RNA data.
        gene_dict: Dictionary mapping gene names to (chromosome, TSS) tuples.

    Returns:
        PyRanges object with columns: Chromosome, Start, End, gene_idx.
    """
    rows = []
    for gene_idx, gene_name in enumerate(adata_rna.var_names):
        if gene_name not in gene_dict:
            continue
        chrom, tss = gene_dict[gene_name]
        rows.append([chrom, tss, tss + 1, gene_idx])
    df_genes = pd.DataFrame(rows, columns=["Chromosome", "Start", "End", "gene_idx"])
    return pr.PyRanges(df_genes)


def build_region_gene_pairs(
    adata_atac, adata_rna, distance1=5_000, distance2=500_000, species="mouse"
):
    """Build array of region-gene pairs with weights based on distance.

    Rules:
    - If distance < 5 kb => weight = 1.0
    - Else if distance < 200 kb => weight = 0
    - Otherwise, exclude the pair
    - Exclusive logic: If a region is within 5 kb of ANY gene => only keep 1.0 pairs

    Args:
        adata_atac: AnnData object with ATAC data.
        adata_rna: AnnData object with RNA data.
        distance1: Distance threshold for weight=1.0 (default: 5kb).
        distance2: Maximum allowed distance (default: 500kb).
        species: Species name for BioMart query (default: "mouse").

    Returns:
        JAX array of shape (N, 3): [region_idx, gene_idx, weight].
    """
    # 1) Build gene TSS dict (using pybiomart)
    if species == "mouse":
        dsname = "mmusculus_gene_ensembl"
    elif species == "human":
        dsname = "hsapiens_gene_ensembl"
    gene_dict = build_gene_tss_dict(adata_rna, dataset_name=dsname)

    # 2) Convert to PyRanges
    gr_regions = build_pyranges_for_regions(adata_atac)
    gr_genes = build_pyranges_for_genes(adata_rna, gene_dict)

    # 3) Expand the gene intervals by ±distance2 => up to 200 kb
    gr_genes_expanded = gr_genes.slack(distance2)

    # 4) Join region intervals with expanded gene intervals => all pairs < 200 kb
    joined = gr_regions.join(gr_genes_expanded)
    df_joined = joined.df

    region_start_col = "Start"
    region_end_col = "End"
    gene_start_col = "Start_b"
    gene_end_col = "End_b"

    if "Start_a" in df_joined.columns:
        region_start_col = "Start_a"
        region_end_col = "End_a"
    if "Start_b" not in df_joined.columns:
        # Possibly "Start" is for genes, "Start_a" for regions
        # We'll guess the columns by checking region_idx vs gene_idx
        if "Start_a" in df_joined.columns and "gene_idx" in df_joined.columns:
            # Then "Start_a", "End_a" might be region, so "Start_b", "End_b" is gene
            # But if we don't see "Start_b", it might be "Start"
            pass
        else:
            # or handle more systematically
            pass

    # 5) Compute distances
    region_mid = (df_joined[region_start_col] + df_joined[region_end_col]) // 2
    gene_tss = (df_joined[gene_start_col] + df_joined[gene_end_col]) // 2
    distance = (region_mid - gene_tss).abs()

    # 6) Assign raw weight
    #    We'll skip rows >= distance2 (200 kb)
    valid_mask = distance < distance2
    df_valid = df_joined[valid_mask].copy()

    # Mark rows < 5 kb => 1.0
    raw_weight = np.full(len(df_valid), 0)
    mask1 = distance[valid_mask] < distance1
    raw_weight[mask1] = 1

    df_valid["weight"] = raw_weight

    # 7) Enforce the exclusive logic:
    #    If a region has any 1.0 link, discard that region's 0 links)
    out_list = []
    grouped = df_valid.groupby("region_idx", sort=False)
    for _, subdf in grouped:
        if (subdf["weight"] == 1.0).any():
            # keep only the 1.0 rows
            keep_rows = subdf[subdf["weight"] == 1.0]
        else:
            # keep 0
            keep_rows = subdf
        out_list.append(keep_rows)

    df_final = pd.concat(out_list, ignore_index=True)

    # 8) Extract columns => [region_idx, gene_idx, weight]
    out_array = df_final[["region_idx", "gene_idx", "weight"]].to_numpy(
        dtype=np.float32
    )

    # Convert to JAX array
    region_gene_pairs = jnp.array(out_array)

    return region_gene_pairs


def construct_region_tf_gene_triplets(region_tf_pairs, region_gene_pairs):
    """Construct region-TF-gene triplets from existing pairs.

    Creates all unique (region, tf, gene) combinations based on existing pairs.

    Args:
        region_tf_pairs: JAX array of shape (num_pairs, 2) with [region_idx, tf_idx].
        region_gene_pairs: JAX array of shape (num_rg_pairs, 3) with [region_idx, gene_idx, score].

    Returns:
        JAX array of shape (P, 3) with [region_idx, tf_idx, gene_idx].
    """
    # Convert JAX arrays to NumPy arrays for preprocessing
    region_tf_pairs_np = np.array(region_tf_pairs)
    region_gene_pairs_np = np.array(region_gene_pairs)

    region_to_tfs = {}
    for pair in region_tf_pairs_np:
        region, tf = pair
        region = int(region)  # Convert to Python int
        tf = int(tf)  # Convert to Python int
        region_to_tfs.setdefault(region, []).append(tf)

    region_to_genes = {}
    for pair in region_gene_pairs_np:
        region, gene = pair[:2]  # Ignore the third column
        region = int(region)  # Convert to Python int
        gene = int(gene)  # Convert to Python int
        region_to_genes.setdefault(region, []).append(gene)

    # Now, create all (region, tf, gene) triplets where tf and gene share the same region
    region_tf_gene_triplets = []
    for region in region_to_tfs:
        tfs = region_to_tfs[region]
        genes = region_to_genes.get(region, [])
        for tf in tfs:
            for gene in genes:
                region_tf_gene_triplets.append([region, tf, gene])

    # Convert the list to a NumPy array and then to a JAX array
    region_tf_gene_triplets_np = np.array(region_tf_gene_triplets, dtype=int)
    region_tf_gene_triplets_jax = jnp.array(region_tf_gene_triplets_np)

    return region_tf_gene_triplets_jax


def rhg_to_rh_indexing(region_tf_gene_triplets, region_tf_pairs):
    """Map region-TF-gene triplets to corresponding region-TF pair indices.

    Args:
        region_tf_gene_triplets: NumPy/JAX array of shape (num_rtg_triplets, 3)
            with [region_idx, tf_idx, gene_idx].
        region_tf_pairs: NumPy/JAX array of shape (num_rt_pairs, 2)
            with [region_idx, tf_idx].

    Returns:
        NumPy array of shape (num_rtg_triplets,) mapping each triplet to its index
        in region_tf_pairs.

    Raises:
        ValueError: If any triplet's [region, tf] pair is not found in region_tf_pairs.
    """
    # Make sure everything is np.array
    region_tf_gene_triplets_np = np.array(region_tf_gene_triplets)
    region_tf_pairs_np = np.array(region_tf_pairs)

    # Transform region-TF pairs from each array (region_idx:tf_idx, e.g. 1:3000)
    rhg_rh = (
        region_tf_gene_triplets_np[:, 0].astype(str)
        + ":"
        + region_tf_gene_triplets_np[:, 1].astype(str)
    )
    rh_rh = (
        region_tf_pairs_np[:, 0].astype(str)
        + ":"
        + region_tf_pairs_np[:, 1].astype(str)
    )

    # Make region-TF-pairs a lookup dictionary
    rh_map = {val: idx for idx, val in enumerate(rh_rh)}

    # Get indices inside region-gene-pairs (rh) for every element in region-tf-gene-triplets (rhg)
    rhg_indices = np.array([rh_map.get(x, -1) for x in rhg_rh])

    # Raise error if -1 is present
    if (rhg_indices == -1).any():
        raise ValueError(
            "Unmapped entries in region_tf_gene_triplets. Not present in region_tf_pairs."
        )

    return rhg_indices
