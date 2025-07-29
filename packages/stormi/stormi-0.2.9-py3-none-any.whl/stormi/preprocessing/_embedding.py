"""Functions for single-cell embedding using scVI and multiVI."""

from typing import Optional, Tuple, Union

from anndata import AnnData
from scvi.model import MULTIVI, SCVI

from stormi.preprocessing._complexity import (
    compute_pca_complexity,
    default_epochs,
    default_n_hidden,
    default_n_latent,
    default_n_layers,
)


def run_scvi(
    adata_rna: AnnData,
    adata_atac: Optional[AnnData] = None,
    latent_key: str = "X_scVI",
    n_hidden: Optional[int] = None,
    n_latent: Optional[int] = None,
    n_layers: Optional[int] = None,
    dropout_rate: Optional[float] = None,
    max_epochs: Optional[int] = None,
    save_model_path: Optional[str] = None,
    variance_threshold: float = 0.9,
    n_comps: int = 50,
    **kwargs,
) -> Union[AnnData, Tuple[AnnData, AnnData]]:
    """Run scVI or multiVI embedding on single-cell data.

    Runs scVI (if only RNA is provided) or multiVI (if both RNA and ATAC are provided)
    on the input AnnData object(s). Hyperparameters are chosen automatically based on the
    number of cells and a measure of dataset complexity (computed via PCA) unless explicitly
    provided by the user.

    Args:
        adata_rna: AnnData object with RNA counts.
        adata_atac: AnnData object with ATAC counts (optional). Must have the same cells
            (and order) as adata_rna.
        latent_key: Key to store the latent representation in .obsm.
        n_hidden: Number of hidden units per layer. Defaults to an automatic choice.
        n_latent: Dimensionality of the latent space. Defaults to an automatic choice.
        n_layers: Number of hidden layers. Defaults to an automatic choice.
        dropout_rate: Dropout rate. Defaults to 0.1.
        max_epochs: Maximum number of training epochs. Defaults to an automatic choice.
        save_model_path: Directory to save the trained model. If None, the model is not saved.
        variance_threshold: Fraction of variance that PCA must explain to define dataset complexity.
        n_comps: Maximum number of PCA components to compute for complexity estimation.
        **kwargs: Additional keyword arguments passed to the model constructor.

    Returns:
        If only RNA is provided, returns the updated adata_rna.
        If ATAC is provided, returns a tuple (adata_rna, adata_atac)
        with the latent representation added.
    """
    n_obs = adata_rna.n_obs
    # Compute a simple complexity measure: #PCs needed to reach variance_threshold
    complexity = compute_pca_complexity(
        adata_rna, variance_threshold=variance_threshold, n_comps=n_comps
    )

    # Set defaults if parameters are not provided.
    if n_hidden is None:
        n_hidden = default_n_hidden(n_obs, complexity)
    if n_latent is None:
        n_latent = default_n_latent(n_obs, complexity)
    if n_layers is None:
        n_layers = default_n_layers(n_obs, complexity)
    if dropout_rate is None:
        dropout_rate = 0.1
    if max_epochs is None:
        max_epochs = default_epochs(n_obs, complexity)

    # Print out chosen hyperparameters
    print("Chosen Hyperparameters:")
    print(f"  - Number of hidden units per layer: {n_hidden}")
    print(f"  - Latent space dimensionality: {n_latent}")
    print(f"  - Number of layers: {n_layers}")
    print(f"  - Dropout rate: {dropout_rate}")
    print(f"  - Maximum training epochs: {max_epochs}")

    # ------------------------ RNA only: SCVI ------------------------
    if adata_atac is None:
        # 1) Set up Anndata specifically for SCVI
        SCVI.setup_anndata(adata_rna)

        # 2) Create and train the SCVI model
        model = SCVI(
            adata=adata_rna,
            n_hidden=n_hidden,
            n_layers=n_layers,
            n_latent=n_latent,
            dropout_rate=dropout_rate,
            **kwargs,
        )
        model.train(max_epochs=max_epochs)

        # 3) Store latent representation
        latent = model.get_latent_representation()
        adata_rna.obsm[latent_key] = latent

        # 4) Save model if path provided
        if save_model_path is not None:
            model.save(save_model_path, overwrite=True)

        return adata_rna

    # --------------------- RNA + ATAC: MULTIVI ----------------------
    else:
        # Ensure consistent cell order
        if not (adata_rna.obs_names == adata_atac.obs_names).all():
            raise ValueError(
                "RNA and ATAC AnnData objects must have the same obs_names in the same order."
            )

        # 1) Create a joint object by copying RNA and storing ATAC in obsm
        adata_joint = adata_rna.copy()
        adata_joint.obsm["X_atac"] = adata_atac.X

        # 2) Set up Anndata specifically for MULTIVI
        MULTIVI.setup_anndata(adata_joint)

        # 3) Create and train the MULTIVI model
        model = MULTIVI(
            adata_joint,
            n_hidden=n_hidden,
            n_layers=n_layers,
            n_latent=n_latent,
            dropout_rate=dropout_rate,
            **kwargs,
        )
        model.train(max_epochs=max_epochs)

        # 4) Store latent representation in both objects
        latent = model.get_latent_representation()
        adata_rna.obsm[latent_key] = latent
        adata_atac.obsm[latent_key] = latent

        # 5) Save model if path provided
        if save_model_path is not None:
            model.save(save_model_path, overwrite=True)

        return adata_rna, adata_atac
