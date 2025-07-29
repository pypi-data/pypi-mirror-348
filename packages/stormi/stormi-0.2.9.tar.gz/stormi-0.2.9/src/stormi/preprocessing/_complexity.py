"""Functions for computing data complexity and auto-selecting model parameters."""

import math

import numpy as np
import scanpy as sc
from anndata import AnnData


def compute_pca_complexity(
    adata: AnnData, variance_threshold: float = 0.9, n_comps: int = 50
) -> int:
    """
    Computes a simple measure of dataset complexity: the number of principal components
    required to explain at least `variance_threshold` of the variance.

    If PCA has not yet been computed, this function runs sc.pp.pca on the adata.
    """
    # Ensure n_comps doesn't exceed dataset dimensions
    n_comps = min(n_comps, adata.n_obs - 1, adata.n_vars - 1)

    if "pca" not in adata.uns:
        sc.pp.pca(adata, n_comps=n_comps)
    variance_ratio = adata.uns["pca"]["variance_ratio"]
    cum_var = np.cumsum(variance_ratio)
    complexity = int(np.searchsorted(cum_var, variance_threshold)) + 1
    return complexity


def default_n_latent(n_obs: int, complexity: int) -> int:
    """Compute a default latent dimension for scVI/multiVI models.

    Base is 20 + 10 * log10(n_obs/1e3) and then adjusted upward by 0.5 * complexity.
    Capped at 150.

    Args:
        n_obs: Number of observations (cells).
        complexity: Dataset complexity measure.

    Returns:
        int: Recommended latent dimension size.
    """
    base = 20 + 10 * math.log10(n_obs / 1000)
    return int(max(20, min(150, base + 0.5 * complexity)))


def default_n_hidden(n_obs: int, complexity: int) -> int:
    """Compute a default number of hidden units per layer.

    Base is 256 + 64 * log10(n_obs/1e3) and then adjusted upward by 8 * complexity.
    Capped at 1024.

    Args:
        n_obs: Number of observations (cells).
        complexity: Dataset complexity measure.

    Returns:
        int: Recommended number of hidden units.
    """
    base = 256 + 64 * math.log10(n_obs / 1000)
    return int(max(256, min(1024, base + 8 * complexity)))


def default_n_layers(n_obs: int, complexity: int) -> int:
    """Return a default number of layers for neural network models.

    For fewer than 1e5 cells, use 2 layers if complexity < 20, else 3.
    For larger datasets, use 3 layers if complexity < 30, else 4.

    Args:
        n_obs: Number of observations (cells).
        complexity: Dataset complexity measure.

    Returns:
        int: Recommended number of layers.
    """
    if n_obs < 1e5:
        return 2 if complexity < 20 else 3
    else:
        return 3 if complexity < 30 else 4


def default_epochs(n_obs: int, complexity: int) -> int:
    """Compute a default number of training epochs.

    Base increases with n_obs and is scaled by the complexity.
    For 1e4 cells with moderate complexity, ~600 epochs are used.
    The final number is increased by a factor (1 + complexity/50)
    to ensure higher iterations for more complex datasets.

    Args:
        n_obs: Number of observations (cells).
        complexity: Dataset complexity measure.

    Returns:
        int: Recommended number of training epochs.
    """
    base = 600 + 200 * math.log10(n_obs / 10000)
    return int(max(400, base * (1 + complexity / 50)))
