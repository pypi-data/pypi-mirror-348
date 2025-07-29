"""Tests for the _filtering module."""

import numpy as np
import pandas as pd
import pytest
from anndata import AnnData

from stormi.preprocessing import filter_genes, filter_motif_scores, filter_regions


@pytest.fixture
def simple_adata_rna():
    """Create a small RNA AnnData object for testing."""
    n_cells, n_genes = 20, 30
    X = np.random.rand(n_cells, n_genes)
    gene_names = [f"gene{i}" for i in range(n_genes)]
    # Add some mitochondrial genes
    gene_names[0] = "MT-gene1"
    gene_names[1] = "mt-gene2"

    adata = AnnData(X=X)
    adata.var_names = pd.Index(gene_names)
    adata.var["gene_type"] = ["protein_coding"] * n_genes

    return adata


@pytest.fixture
def simple_adata_atac():
    """Create a small ATAC AnnData object for testing."""
    n_cells, n_peaks = 20, 40
    X = np.random.rand(n_cells, n_peaks)
    peak_names = [f"chr1:{i * 1000}-{i * 1000 + 500}" for i in range(n_peaks)]

    adata = AnnData(X=X)
    adata.var_names = pd.Index(peak_names)

    return adata


@pytest.fixture
def simple_motif_scores():
    """Create simple motif scores for testing."""
    genes = [f"gene{i}" for i in range(5)]
    peaks = [f"chr1:{i * 1000}-{i * 1000 + 500}" for i in range(8)]

    data = []
    for gene in genes:
        for peak in peaks:
            data.append({"gene": gene, "peak": peak, "score": np.random.rand()})

    return pd.DataFrame(data)


def test_filter_genes(simple_adata_rna):
    """Test filtering genes from an AnnData object."""
    # Basic filtering
    filtered = filter_genes(simple_adata_rna)

    # Check that mitochondrial genes are removed when requested
    assert filtered.shape[1] < simple_adata_rna.shape[1]
    assert not any(g.startswith(("MT-", "mt-")) for g in filtered.var_names)


def test_filter_regions(simple_adata_atac):
    """Test filtering regions from an AnnData object."""
    # Set some regions to be detected in few cells
    X_sparse = simple_adata_atac.X.copy()
    X_sparse[:, 0] = np.zeros(simple_adata_atac.shape[0])  # No cells have this peak
    X_sparse[:, 1] = np.zeros(simple_adata_atac.shape[0])
    X_sparse[0, 1] = 1  # Only one cell has this peak
    simple_adata_atac.X = X_sparse

    # Filter with min_cells=2 and score_percentile=0.0 (disable score-based filtering)
    filtered = filter_regions(simple_adata_atac, min_cells=2, score_percentile=0.0)

    # Check that only the regions with less than min_cells were filtered
    assert filtered.shape[1] == simple_adata_atac.shape[1] - 2


def test_filter_motif_scores(simple_adata_rna, simple_adata_atac, simple_motif_scores):
    """Test filtering motif scores based on genes and regions."""
    # Create a motif_scores DataFrame in the expected format (with TF names as index)
    # First get a subset of genes and peaks
    rna_genes = simple_adata_rna.var_names[:3]
    atac_peaks = simple_adata_atac.var_names[:3]

    # Subset RNA and ATAC data to these genes and peaks
    subset_rna = simple_adata_rna[:, rna_genes]
    subset_atac = simple_adata_atac[:, atac_peaks]

    # Create motif scores with TFs as index and peaks as columns
    tf_peak_data = {}
    for peak in atac_peaks:
        tf_peak_data[peak] = np.random.rand(len(rna_genes))

    motif_df = pd.DataFrame(tf_peak_data, index=rna_genes)

    # Call the filter_motif_scores function
    filtered_scores = filter_motif_scores(motif_df, subset_rna, subset_atac)

    # Check filtering worked correctly
    assert set(filtered_scores.index) <= set(subset_rna.var_names)
    assert set(filtered_scores.columns) <= set(subset_atac.var_names)
