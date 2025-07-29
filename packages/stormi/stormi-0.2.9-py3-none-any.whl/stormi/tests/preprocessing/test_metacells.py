"""Tests for the _metacells module."""

import numpy as np
import pandas as pd
import pytest
import scipy.sparse as sp
from anndata import AnnData

from stormi.preprocessing import compute_metacells, convert_to_dense


@pytest.fixture
def simple_adata_rna_with_clusters():
    """Create a small AnnData object with clusters for testing."""
    n_cells, n_genes = 50, 100
    X = np.random.rand(n_cells, n_genes)
    adata = AnnData(X=X)

    # Add clustering information
    adata.obs["leiden"] = np.repeat(["0", "1", "2", "3", "4"], 10)

    # Add latent representation
    adata.obsm["X_scVI"] = np.random.rand(n_cells, 10)

    return adata


@pytest.fixture
def simple_adata_atac_with_clusters():
    """Create a small ATAC AnnData object with the same cells and clusters."""
    n_cells, n_peaks = 50, 200
    X = np.random.rand(n_cells, n_peaks)
    adata = AnnData(X=X)

    # Add clustering information
    adata.obs["leiden"] = np.repeat(["0", "1", "2", "3", "4"], 10)

    return adata


def test_convert_to_dense():
    """Test converting sparse matrices to dense arrays."""
    # Test with dense array
    dense_array = np.random.rand(10, 20)
    result_dense = convert_to_dense(dense_array)
    assert np.array_equal(result_dense, dense_array)

    # Test with sparse matrix
    sparse_matrix = sp.csr_matrix(dense_array)
    result_sparse = convert_to_dense(sparse_matrix)
    assert np.array_equal(result_sparse, dense_array)


@pytest.mark.skipif(
    True,
    reason="Skipping metacell tests as they require scanpy/clustering dependencies",
)
def test_compute_metacells_rna_only(simple_adata_rna_with_clusters):
    """Test computing metacells from RNA data only."""
    # Make the test small for speed
    simple_adata_rna_with_clusters = simple_adata_rna_with_clusters[:20].copy()

    # Run compute_metacells
    metacells = compute_metacells(
        adata_rna=simple_adata_rna_with_clusters,
        latent_key="X_scVI",
    )

    # Check metacell structure
    assert isinstance(metacells, AnnData)
    assert metacells.n_obs <= simple_adata_rna_with_clusters.n_obs
    assert metacells.n_vars == simple_adata_rna_with_clusters.n_vars
    assert "n_cells" in metacells.obs


@pytest.mark.skipif(
    True,
    reason="Skipping metacell tests as they require scanpy/clustering dependencies",
)
def test_compute_metacells_multimodal(
    simple_adata_rna_with_clusters, simple_adata_atac_with_clusters
):
    """Test computing metacells from both RNA and ATAC data."""
    # Make the test small for speed
    simple_adata_rna_with_clusters = simple_adata_rna_with_clusters[:20].copy()
    simple_adata_atac_with_clusters = simple_adata_atac_with_clusters[:20].copy()

    # Use the same observation names for RNA and ATAC
    obs_names = [f"cell_{i}" for i in range(20)]
    simple_adata_rna_with_clusters.obs_names = obs_names
    simple_adata_atac_with_clusters.obs_names = obs_names

    # Run compute_metacells
    metacells_rna, metacells_atac = compute_metacells(
        adata_rna=simple_adata_rna_with_clusters,
        adata_atac=simple_adata_atac_with_clusters,
        latent_key="X_scVI",
    )

    # Check metacell structure
    assert isinstance(metacells_rna, AnnData)
    assert isinstance(metacells_atac, AnnData)
    assert metacells_rna.n_obs == metacells_atac.n_obs
    assert metacells_rna.n_vars == simple_adata_rna_with_clusters.n_vars
    assert metacells_atac.n_vars == simple_adata_atac_with_clusters.n_vars
    assert "n_cells" in metacells_rna.obs
    assert "n_cells" in metacells_atac.obs
