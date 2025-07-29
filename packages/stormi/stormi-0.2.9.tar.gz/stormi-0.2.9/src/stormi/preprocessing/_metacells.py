"""Functions for computing and working with metacells."""

import logging
import warnings
from typing import List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scanpy as sc
import scanpy.external as sce
import scipy.sparse as sp
from anndata import AnnData
from beartype import beartype
from scipy.sparse import csr_matrix

logger = logging.getLogger(__name__)


@beartype
def convert_to_dense(layer):
    """Convert a sparse matrix to a dense numpy array.

    Args:
        layer: Input array or sparse matrix.

    Returns:
        Dense numpy array.
    """
    if sp.issparse(layer):
        return layer.toarray()
    else:
        return layer


@beartype
def compute_metacells(
    adata_rna: "AnnData",
    adata_atac: Optional["AnnData"] = None,
    latent_key: str = "X_scVI",
    invariant_keys: List[str] = [],
    merge_categorical_keys: List[str] = [],
    numerical_keys: List[str] = [],
    n_neighbors: int = 10,
    resolution: int = 50,
    verbose: bool = True,
    merge_umap: bool = True,
    umap_key: Optional[str] = None,
) -> Union["AnnData", Tuple["AnnData", "AnnData"]]:
    """Compute metacells by clustering cells in a latent space.

    Clusters cells in a latent space and merges counts and metadata to create metacells.
    If ATAC data is provided, both RNA and ATAC metacells are computed and returned.
    Otherwise, only RNA metacells are computed.

    All .var and .uns fields are copied from the original objects.

    Args:
        adata_rna: AnnData object with RNA counts.
        adata_atac: AnnData object with ATAC counts (optional).
        latent_key: Name of latent space key in .obsm of adata_rna.
        invariant_keys: List of categorical keys in adata_rna.obs that must be homogeneous
            within a metacell.
        merge_categorical_keys: List of categorical keys in adata_rna.obs that can be merged.
        numerical_keys: List of numerical keys in adata_rna.obs to be averaged in each metacell.
        n_neighbors: Number of nearest neighbors for the cell–cell graph.
        resolution: Resolution parameter for Leiden clustering.
        verbose: Whether to print progress and diagnostic plots.
        merge_umap: Whether to merge UMAP coordinates for metacells.
        umap_key: Key for UMAP embedding in adata_rna.obsm.

    Returns:
        If adata_atac is None: returns the merged RNA AnnData object.
        Otherwise: returns a tuple (rna_metacell, atac_metacell).
    """
    # Ensure RNA data is in sparse format and add total counts.
    if not isinstance(adata_rna.X, csr_matrix):
        adata_rna.X = csr_matrix(adata_rna.X)
    adata_rna.obs["RNA counts"] = np.array(adata_rna.X.sum(axis=1)).ravel()

    # Process ATAC data if provided.
    if adata_atac is not None:
        if len(adata_rna.obs_names) != len(adata_atac.obs_names):
            raise ValueError("RNA and ATAC data do not have the same number of cells.")
        if not (adata_rna.obs_names == adata_atac.obs_names).all():
            raise ValueError(
                "RNA and ATAC data do not contain the same cells in obs_names."
            )
        if not isinstance(adata_atac.X, csr_matrix):
            adata_atac.X = csr_matrix(adata_atac.X)
        adata_atac = adata_atac[adata_rna.obs_names, :]
        adata_atac.obs["ATAC counts"] = np.array(adata_atac.X.sum(axis=1)).ravel()

    # --- CLUSTERING STEP on RNA ---
    if verbose:
        print("Computing neighbors and running Leiden clustering on RNA data...")
    sc.pp.neighbors(adata_rna, use_rep=latent_key, n_neighbors=n_neighbors)
    sc.tl.leiden(adata_rna, key_added="leiden", resolution=resolution)

    # Define metacell labels.
    if invariant_keys:
        combined = adata_rna.obs[invariant_keys].astype(str).agg("_".join, axis=1)
        adata_rna.obs["metacell"] = adata_rna.obs["leiden"].astype(str) + "_" + combined
    else:
        adata_rna.obs["metacell"] = adata_rna.obs["leiden"]

    if adata_atac is not None:
        adata_atac.obs["metacell"] = adata_rna.obs["metacell"]
    cluster_key = "metacell"

    if verbose:
        counts = adata_rna.obs[cluster_key].value_counts()
        print("Total number of cells:", adata_rna.n_obs)
        print("Total number of metacells:", len(counts))
        print(
            "Cells per metacell -- min: {}, mean: {:.1f}, max: {}".format(
                counts.min(), counts.mean(), counts.max()
            )
        )
        plt.hist(counts, bins=10)
        plt.xlabel("Cells per metacell")
        plt.ylabel("Number of metacells")
        plt.show()

    # --- MERGE FUNCTIONS ---
    @beartype
    def merge_RNA(
        adata_rna: "AnnData",
        cluster_key: str,
        invariant_keys: List[str],
        merge_categorical_keys: List[str],
        numerical_keys: List[str],
        verbose: bool = True,
    ) -> "AnnData":
        """Merge RNA data by clusters to create metacells.

        Args:
            adata_rna: AnnData object with RNA expression.
            cluster_key: Column in adata_rna.obs indicating cluster membership.
            invariant_keys: Categorical keys that must be homogeneous within a metacell.
            merge_categorical_keys: Categorical keys that can be merged (using mode).
            numerical_keys: Numerical keys to be averaged.
            verbose: Whether to print progress information.

        Returns:
            AnnData object containing merged metacells.
        """
        if verbose:
            print("Merging RNA counts...")
        clusters = np.unique(adata_rna.obs[cluster_key])
        merged_X_list = []
        n_cells_list = []
        merged_annots = {
            key: []
            for key in (invariant_keys + merge_categorical_keys + numerical_keys)
        }

        for c in clusters:
            idx = adata_rna.obs[cluster_key] == c
            X_sum = np.array(adata_rna.X[idx, :].sum(axis=0)).ravel()
            merged_X_list.append(X_sum)
            n_cells = int(idx.sum())
            n_cells_list.append(n_cells)

            for key in invariant_keys:
                unique_vals = adata_rna.obs.loc[idx, key].unique()
                if len(unique_vals) != 1:
                    raise ValueError(
                        f"Metacell {c} is not homogeneous for invariant key '{key}'. Found: {unique_vals}"
                    )
                merged_annots[key].append(unique_vals[0])
            for key in merge_categorical_keys:
                mode_val = adata_rna.obs.loc[idx, key].mode()[0]
                merged_annots[key].append(mode_val)
            for key in numerical_keys:
                avg_val = adata_rna.obs.loc[idx, key].mean()
                merged_annots[key].append(avg_val)

        merged_X = np.vstack(merged_X_list)
        adata_meta = sc.AnnData(X=merged_X)
        adata_meta.var = adata_rna.var.copy()
        # Copy the unstructured data
        adata_meta.uns = adata_rna.uns.copy() if hasattr(adata_rna, "uns") else {}

        meta_obs = pd.DataFrame(index=clusters)
        meta_obs["n_cells"] = n_cells_list
        for key in invariant_keys + merge_categorical_keys + numerical_keys:
            meta_obs[key] = merged_annots[key]
        meta_obs["RNA counts"] = merged_X.sum(axis=1)
        adata_meta.obs = meta_obs

        # Merge additional layers if present.
        for layer in ["unspliced", "spliced"]:
            if layer in adata_rna.layers:
                layer_list = []
                for c in clusters:
                    idx = adata_rna.obs[cluster_key] == c
                    layer_sum = np.array(
                        adata_rna.layers[layer][idx, :].sum(axis=0)
                    ).ravel()
                    layer_list.append(layer_sum)
                merged_layer = np.vstack(layer_list)
                adata_meta.layers[layer] = csr_matrix(merged_layer, dtype=np.uint16)

        if verbose:
            print(
                "Mean RNA counts per cell before:", np.mean(adata_rna.obs["RNA counts"])
            )
            print(
                "Mean RNA counts per metacell after:",
                np.mean(adata_meta.obs["RNA counts"]),
            )
            plt.hist(
                adata_rna.obs["RNA counts"], bins=10, label="Single cells", alpha=0.5
            )
            plt.hist(
                adata_meta.obs["RNA counts"], bins=20, label="Metacells", alpha=0.5
            )
            plt.xlabel("Total RNA Counts")
            plt.ylabel("Frequency")
            plt.legend()
            plt.show()
        return adata_meta

    @beartype
    def merge_UMAP(
        adata_rna: "AnnData",
        adata_meta: "AnnData",
        cluster_key: str,
        umap_key: str = "X_umap",
        verbose: bool = True,
    ) -> "AnnData":
        """Merge UMAP coordinates for metacells.

        Args:
            adata_rna: Original AnnData object with UMAP coordinates.
            adata_meta: Metacell AnnData object to update.
            cluster_key: Column in adata_rna.obs indicating cluster membership.
            umap_key: Key for UMAP embedding in adata_rna.obsm.
            verbose: Whether to print progress information.

        Returns:
            Updated metacell AnnData object with UMAP coordinates.
        """
        if verbose:
            print("Merging UMAP coordinates...")
        clusters = np.unique(adata_rna.obs[cluster_key])
        umap_list = []
        for c in clusters:
            idx = adata_rna.obs[cluster_key] == c
            coord = np.mean(adata_rna.obsm[umap_key][idx, :], axis=0)
            umap_list.append(coord)
        adata_meta.obsm[umap_key] = np.vstack(umap_list)
        return adata_meta

    @beartype
    def merge_ATAC(
        adata_atac: "AnnData",
        cluster_key: str,
        invariant_keys: List[str],
        merge_categorical_keys: List[str],
        numerical_keys: List[str],
        verbose: bool = True,
    ) -> "AnnData":
        """Merge ATAC data by clusters to create metacells.

        Args:
            adata_atac: AnnData object with ATAC data.
            cluster_key: Column in adata_atac.obs indicating cluster membership.
            invariant_keys: Categorical keys that must be homogeneous within a metacell.
            merge_categorical_keys: Categorical keys that can be merged (using mode).
            numerical_keys: Numerical keys to be averaged.
            verbose: Whether to print progress information.

        Returns:
            AnnData object containing merged ATAC metacells.
        """
        if verbose:
            print("Merging ATAC counts...")
        clusters = np.unique(adata_atac.obs[cluster_key])
        merged_X_list = []
        n_cells_list = []
        merged_annots = {
            key: []
            for key in (invariant_keys + merge_categorical_keys + numerical_keys)
        }

        for c in clusters:
            idx = adata_atac.obs[cluster_key] == c
            X_sum = np.array(adata_atac.X[idx, :].sum(axis=0)).ravel()
            merged_X_list.append(X_sum)
            n_cells = int(idx.sum())
            n_cells_list.append(n_cells)
            for key in invariant_keys:
                unique_vals = adata_atac.obs.loc[idx, key].unique()
                if len(unique_vals) != 1:
                    raise ValueError(
                        f"Metacell {c} is not homogeneous for invariant key '{key}'. Found: {unique_vals}"
                    )
                merged_annots[key].append(unique_vals[0])
            for key in merge_categorical_keys:
                mode_val = adata_atac.obs.loc[idx, key].mode()[0]
                merged_annots[key].append(mode_val)
            for key in numerical_keys:
                avg_val = adata_atac.obs.loc[idx, key].mean()
                merged_annots[key].append(avg_val)

        merged_X = np.vstack(merged_X_list)
        adata_meta = sc.AnnData(X=merged_X)
        adata_meta.var = adata_atac.var.copy()
        # Copy over unstructured data
        adata_meta.uns = adata_atac.uns.copy() if hasattr(adata_atac, "uns") else {}

        meta_obs = pd.DataFrame(index=clusters)
        meta_obs["n_cells"] = n_cells_list
        for key in invariant_keys + merge_categorical_keys + numerical_keys:
            meta_obs[key] = merged_annots[key]
        meta_obs["ATAC counts"] = merged_X.sum(axis=1)
        adata_meta.obs = meta_obs

        if verbose:
            print(
                "Mean ATAC counts per cell before:",
                np.mean(adata_atac.obs["ATAC counts"]),
            )
            print(
                "Mean ATAC counts per metacell after:",
                np.mean(adata_meta.obs["ATAC counts"]),
            )
            plt.hist(
                adata_atac.obs["ATAC counts"], bins=10, label="Single cells", alpha=0.5
            )
            plt.hist(
                adata_meta.obs["ATAC counts"], bins=20, label="Metacells", alpha=0.5
            )
            plt.xlabel("Total ATAC Counts")
            plt.ylabel("Frequency")
            plt.legend()
            plt.show()
        return adata_meta

    # --- MERGE RNA METACELLS ---
    adata_meta_rna = merge_RNA(
        adata_rna,
        cluster_key=cluster_key,
        invariant_keys=invariant_keys,
        merge_categorical_keys=merge_categorical_keys,
        numerical_keys=numerical_keys,
        verbose=verbose,
    )

    if merge_umap:
        if not umap_key or umap_key not in adata_rna.obsm:
            if verbose:
                warnings.warn(
                    "UMAP embedding not found; computing with sc.tl.umap()...",
                    UserWarning,
                )
            sc.tl.umap(adata_rna)
            umap_key = "X_umap"
        adata_meta_rna = merge_UMAP(
            adata_rna,
            adata_meta_rna,
            cluster_key=cluster_key,
            umap_key=umap_key,
            verbose=verbose,
        )

    # --- MERGE ATAC METACELLS if provided ---
    if adata_atac is not None:
        adata_meta_atac = merge_ATAC(
            adata_atac,
            cluster_key=cluster_key,
            invariant_keys=invariant_keys,
            merge_categorical_keys=merge_categorical_keys,
            numerical_keys=numerical_keys,
            verbose=verbose,
        )
        # Optionally copy ATAC counts into the RNA metacell object.
        adata_meta_rna.obs["ATAC counts"] = adata_meta_atac.obs["ATAC counts"]
        if verbose:
            print("Metacell construction complete for both RNA and ATAC data.")
        return adata_meta_rna, adata_meta_atac
    else:
        if verbose:
            print("Metacell construction complete for RNA data only.")
        return adata_meta_rna


@beartype
def create_metacells(
    data_rna: AnnData,
    data_atac: AnnData,
    grouping_key: str,
    resolution: int,
    batch_key: str,
) -> Tuple[AnnData, AnnData]:
    """Create metacells by clustering and summarizing expression.

    This function:
    1) Normalizes data, runs PCA + harmony integration on batch_key
    2) Clusters using leiden => store in data_rna.obs[grouping_key]
    3) Summarizes expression & accessibility per cluster => metacell

    Args:
        data_rna: AnnData object with RNA counts.
        data_atac: AnnData object with ATAC counts.
        grouping_key: Key to store the cluster labels in data_rna.obs.
        resolution: Resolution parameter for Leiden clustering.
        batch_key: Column in data_rna.obs to use for batch correction.

    Returns:
        Tuple containing (rna_metacell, atac_metacell) AnnData objects.
    """
    logger.info(
        f"Creating metacells with resolution={resolution} (grouping key={grouping_key})."
    )
    # Keep original counts in a layer
    data_rna.layers["counts"] = data_rna.X.copy()

    # Normalize & run PCA
    sc.pp.normalize_total(data_rna)
    sc.pp.log1p(data_rna)
    sc.pp.pca(data_rna)

    # Harmony integration
    sce.pp.harmony_integrate(data_rna, batch_key)

    sc.pp.neighbors(data_rna, use_rep="X_pca_harmony")
    sc.tl.leiden(data_rna, resolution=resolution, key_added=grouping_key)

    # Summarize
    clusters = data_rna.obs[grouping_key].unique()
    cluster_groups = data_rna.obs.groupby(grouping_key)

    mean_rna_list = []
    mean_atac_list = []
    cluster_names = []

    for cluster_name in clusters:
        cell_idx = cluster_groups.get_group(cluster_name).index

        # RNA
        rna_vals = data_rna[cell_idx].X
        if sp.issparse(rna_vals):
            # Convert to dense
            rna_vals = rna_vals.toarray()
        mean_rna = np.array(rna_vals.mean(axis=0)).ravel()
        mean_rna_list.append(mean_rna)

        # ATAC
        if len(set(cell_idx).intersection(data_atac.obs_names)) == 0:
            mean_atac_list.append(np.zeros(data_atac.shape[1]))
        else:
            atac_vals = data_atac[cell_idx].X

            if sp.issparse(atac_vals):
                # Convert to dense
                atac_vals = atac_vals.toarray()
            # get fragment values from insertions
            atac_bin = (atac_vals + 1) // 2
            mean_atac = np.array(atac_bin.mean(axis=0)).ravel()
            mean_atac_list.append(mean_atac)

        cluster_names.append(cluster_name)

    # Build new AnnData
    mean_rna_arr = np.vstack(mean_rna_list)
    mean_atac_arr = np.vstack(mean_atac_list)

    obs_df = pd.DataFrame({grouping_key: cluster_names}).set_index(grouping_key)

    rna_metacell = AnnData(X=mean_rna_arr, obs=obs_df, var=data_rna.var)
    atac_metacell = AnnData(X=mean_atac_arr, obs=obs_df, var=data_atac.var)

    logger.info(
        f"Metacell shapes: RNA={rna_metacell.shape}, ATAC={atac_metacell.shape}"
    )
    return rna_metacell, atac_metacell
