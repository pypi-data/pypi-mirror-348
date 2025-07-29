"""Tests for the _complexity module."""

import numpy as np
import pytest
from anndata import AnnData

from stormi.preprocessing import (
    compute_pca_complexity,
    default_epochs,
    default_n_hidden,
    default_n_latent,
    default_n_layers,
)


@pytest.fixture
def simple_adata():
    """Create a small AnnData object for testing."""
    n_cells, n_genes = 20, 100
    X = np.random.rand(n_cells, n_genes)
    return AnnData(X=X)


def test_compute_pca_complexity(simple_adata):
    """Test that compute_pca_complexity returns a reasonable value."""
    complexity = compute_pca_complexity(simple_adata)
    assert isinstance(complexity, int)
    assert complexity > 0


def test_default_functions():
    """Test that the default parameter functions return reasonable values."""
    n_obs = 5000
    complexity = 15

    # Test default_n_latent
    n_latent = default_n_latent(n_obs, complexity)
    assert isinstance(n_latent, int)
    assert n_latent > 0

    # Test default_n_hidden
    n_hidden = default_n_hidden(n_obs, complexity)
    assert isinstance(n_hidden, int)
    assert n_hidden > 0

    # Test default_n_layers
    n_layers = default_n_layers(n_obs, complexity)
    assert isinstance(n_layers, int)
    assert 2 <= n_layers <= 4

    # Test default_epochs
    epochs = default_epochs(n_obs, complexity)
    assert isinstance(epochs, int)
    assert epochs > 0
