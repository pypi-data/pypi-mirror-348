"""Tests for the _embedding module."""

import numpy as np
import pytest
from anndata import AnnData

from stormi.preprocessing import run_scvi


@pytest.fixture
def simple_adata_rna():
    """Create a small AnnData object for testing."""
    n_cells, n_genes = 30, 100
    X = np.random.rand(n_cells, n_genes)
    adata = AnnData(X=X)
    return adata


@pytest.fixture
def simple_adata_atac():
    """Create a small ATAC AnnData object matching RNA cells."""
    n_cells, n_peaks = 30, 200
    X = np.random.rand(n_cells, n_peaks)
    adata = AnnData(X=X)
    return adata


@pytest.mark.skipif(
    True, reason="Skipping test_run_scvi as it requires external ML dependencies"
)
def test_run_scvi_rna_only(simple_adata_rna):
    """Test running scVI on RNA data only."""
    # Mock setup_anndata if needed
    # This test is marked to skip by default since it requires scvi-tools

    result = run_scvi(
        adata_rna=simple_adata_rna,
        n_hidden=10,  # Small network for quick testing
        n_latent=5,
        n_layers=1,
        max_epochs=1,  # Just check it runs, not that it converges
    )

    # Check results
    assert "X_scVI" in result.obsm
    assert result.obsm["X_scVI"].shape == (simple_adata_rna.n_obs, 5)


@pytest.mark.skipif(
    True,
    reason="Skipping test_run_scvi_multimodal as it requires external ML dependencies",
)
def test_run_scvi_multimodal(simple_adata_rna, simple_adata_atac):
    """Test running multiVI with both RNA and ATAC data."""
    # Set matching observation names for RNA and ATAC
    obs_names = [f"cell_{i}" for i in range(simple_adata_rna.n_obs)]
    simple_adata_rna.obs_names = obs_names
    simple_adata_atac.obs_names = obs_names

    # Mock setup_anndata if needed
    # This test is marked to skip by default since it requires scvi-tools

    result_rna, result_atac = run_scvi(
        adata_rna=simple_adata_rna,
        adata_atac=simple_adata_atac,
        n_hidden=10,  # Small network for quick testing
        n_latent=5,
        n_layers=1,
        max_epochs=1,  # Just check it runs, not that it converges
    )

    # Check results
    assert "X_scVI" in result_rna.obsm
    assert "X_scVI" in result_atac.obsm
    assert result_rna.obsm["X_scVI"].shape == (simple_adata_rna.n_obs, 5)
    assert result_atac.obsm["X_scVI"].shape == (simple_adata_atac.n_obs, 5)
    assert np.array_equal(result_rna.obsm["X_scVI"], result_atac.obsm["X_scVI"])
