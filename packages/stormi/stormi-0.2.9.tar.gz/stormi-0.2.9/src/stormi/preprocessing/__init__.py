"""Stormi preprocessing subpackage for processing RNA and ATAC-seq data.

This module provides functions for preprocessing single-cell RNA and ATAC-seq data,
including filtering, dimensionality reduction, metacell computation, and regulatory
element analysis.

Note: This module requires additional dependencies that are not installed by default.
Install them with: pip install stormi[preprocessing]
"""

import importlib
import logging

logger = logging.getLogger(__name__)

HAS_PREPROCESSING_DEPENDENCIES = True
MISSING_DEPENDENCIES = []


def _check_dependency(module_name: str) -> bool:
    """Check if a dependency is available."""
    global HAS_PREPROCESSING_DEPENDENCIES, MISSING_DEPENDENCIES
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        HAS_PREPROCESSING_DEPENDENCIES = False
        MISSING_DEPENDENCIES.append(module_name)
        return False


_has_pyranges = _check_dependency("pyranges")
_has_pybiomart = _check_dependency("pybiomart")
_has_tangermeme = _check_dependency("tangermeme")
_has_gtfparse = _check_dependency("gtfparse")

if not HAS_PREPROCESSING_DEPENDENCIES:
    deps_str = ", ".join(MISSING_DEPENDENCIES)
    logger.warning(
        f"Some preprocessing dependencies are not available: {deps_str}. "
        "Some preprocessing functions will not work. "
        "Install the missing dependencies with: pip install stormi[preprocessing]"
    )

__all__ = [
    # Complexity module
    "compute_pca_complexity",
    "default_n_latent",
    "default_n_hidden",
    "default_n_layers",
    "default_epochs",
    # Embedding module
    "run_scvi",
    # Metacells module
    "compute_metacells",
    "convert_to_dense",
    "create_metacells",
    # Filtering module
    "filter_genes",
    "filter_regions",
    "filter_motif_scores",
    "func_mitochondrial_genes",
    "func_protein_coding_genes",
    "TF_HVG_selection",
    "select_highly_variable_peaks_by_std",
    "keep_promoters_and_select_hv_peaks",
    "bed_file_intersection",
    "simple_bed_intersection",
    # Motifs module
    "compute_motif_scores",
    "compute_in_silico_chipseq",
    # File utils module
    "create_dir_if_not_exists",
    "download_file",
    "unzip_gz",
    "resolve_genome_urls",
    "download_genome_references",
    "check_command_availability",
    # Region-gene-TF module
    "extract_region_tf_pairs",
    "build_gene_tss_dict",
    "parse_region_name",
    "build_pyranges_for_regions",
    "build_pyranges_for_genes",
    "build_region_gene_pairs",
    "construct_region_tf_gene_triplets",
    "rhg_to_rh_indexing",
    # Pipeline module
    "make_multiomic_dataset",
    "pipeline_setup_multiview",
    "preprocessing_pipeline",
]

if HAS_PREPROCESSING_DEPENDENCIES:
    from stormi.preprocessing._complexity import (
        compute_pca_complexity,
        default_epochs,
        default_n_hidden,
        default_n_latent,
        default_n_layers,
    )
    from stormi.preprocessing._embedding import run_scvi
    from stormi.preprocessing._file_utils import (
        check_command_availability,
        create_dir_if_not_exists,
        download_file,
        download_genome_references,
        resolve_genome_urls,
        unzip_gz,
    )
    from stormi.preprocessing._filtering import (
        TF_HVG_selection,
        bed_file_intersection,
        filter_genes,
        filter_motif_scores,
        filter_regions,
        func_mitochondrial_genes,
        func_protein_coding_genes,
        keep_promoters_and_select_hv_peaks,
        select_highly_variable_peaks_by_std,
        simple_bed_intersection,
    )
    from stormi.preprocessing._metacells import (
        compute_metacells,
        convert_to_dense,
        create_metacells,
    )
    from stormi.preprocessing._motifs import (
        compute_in_silico_chipseq,
        compute_motif_scores,
    )
    from stormi.preprocessing._pipeline import (
        preprocessing_pipeline,
    )
    from stormi.preprocessing._region_gene_tf import (
        build_gene_tss_dict,
        build_pyranges_for_genes,
        build_pyranges_for_regions,
        build_region_gene_pairs,
        construct_region_tf_gene_triplets,
        extract_region_tf_pairs,
        parse_region_name,
        rhg_to_rh_indexing,
    )
else:

    def _missing_dependencies_error(func_name):
        deps_str = ", ".join(MISSING_DEPENDENCIES)
        raise ImportError(
            f"Cannot use {func_name} because some preprocessing dependencies are missing: {deps_str}. "
            "Install the missing dependencies with: pip install stormi[preprocessing]"
        )

    def compute_pca_complexity(*args, **kwargs):
        _missing_dependencies_error("compute_pca_complexity")

    def default_n_latent(*args, **kwargs):
        _missing_dependencies_error("default_n_latent")

    def default_n_hidden(*args, **kwargs):
        _missing_dependencies_error("default_n_hidden")

    def default_n_layers(*args, **kwargs):
        _missing_dependencies_error("default_n_layers")

    def default_epochs(*args, **kwargs):
        _missing_dependencies_error("default_epochs")

    def run_scvi(*args, **kwargs):
        _missing_dependencies_error("run_scvi")

    def compute_metacells(*args, **kwargs):
        _missing_dependencies_error("compute_metacells")

    def convert_to_dense(*args, **kwargs):
        _missing_dependencies_error("convert_to_dense")

    def create_metacells(*args, **kwargs):
        _missing_dependencies_error("create_metacells")

    def filter_genes(*args, **kwargs):
        _missing_dependencies_error("filter_genes")

    def filter_regions(*args, **kwargs):
        _missing_dependencies_error("filter_regions")

    def filter_motif_scores(*args, **kwargs):
        _missing_dependencies_error("filter_motif_scores")

    def func_mitochondrial_genes(*args, **kwargs):
        _missing_dependencies_error("func_mitochondrial_genes")

    def func_protein_coding_genes(*args, **kwargs):
        _missing_dependencies_error("func_protein_coding_genes")

    def TF_HVG_selection(*args, **kwargs):
        _missing_dependencies_error("TF_HVG_selection")

    def select_highly_variable_peaks_by_std(*args, **kwargs):
        _missing_dependencies_error("select_highly_variable_peaks_by_std")

    def keep_promoters_and_select_hv_peaks(*args, **kwargs):
        _missing_dependencies_error("keep_promoters_and_select_hv_peaks")

    def bed_file_intersection(*args, **kwargs):
        _missing_dependencies_error("bed_file_intersection")

    def simple_bed_intersection(*args, **kwargs):
        _missing_dependencies_error("simple_bed_intersection")

    def compute_motif_scores(*args, **kwargs):
        _missing_dependencies_error("compute_motif_scores")

    def compute_in_silico_chipseq(*args, **kwargs):
        _missing_dependencies_error("compute_in_silico_chipseq")

    def create_dir_if_not_exists(*args, **kwargs):
        _missing_dependencies_error("create_dir_if_not_exists")

    def download_file(*args, **kwargs):
        _missing_dependencies_error("download_file")

    def unzip_gz(*args, **kwargs):
        _missing_dependencies_error("unzip_gz")

    def resolve_genome_urls(*args, **kwargs):
        _missing_dependencies_error("resolve_genome_urls")

    def download_genome_references(*args, **kwargs):
        _missing_dependencies_error("download_genome_references")

    def check_command_availability(*args, **kwargs):
        _missing_dependencies_error("check_command_availability")

    def extract_region_tf_pairs(*args, **kwargs):
        _missing_dependencies_error("extract_region_tf_pairs")

    def build_gene_tss_dict(*args, **kwargs):
        _missing_dependencies_error("build_gene_tss_dict")

    def parse_region_name(*args, **kwargs):
        _missing_dependencies_error("parse_region_name")

    def build_pyranges_for_regions(*args, **kwargs):
        _missing_dependencies_error("build_pyranges_for_regions")

    def build_pyranges_for_genes(*args, **kwargs):
        _missing_dependencies_error("build_pyranges_for_genes")

    def build_region_gene_pairs(*args, **kwargs):
        _missing_dependencies_error("build_region_gene_pairs")

    def construct_region_tf_gene_triplets(*args, **kwargs):
        _missing_dependencies_error("construct_region_tf_gene_triplets")

    def rhg_to_rh_indexing(*args, **kwargs):
        _missing_dependencies_error("rhg_to_rh_indexing")

    def make_multiomic_dataset(*args, **kwargs):
        _missing_dependencies_error("make_multiomic_dataset")

    def pipeline_setup_multiview(*args, **kwargs):
        _missing_dependencies_error("pipeline_setup_multiview")

    def preprocessing_pipeline(*args, **kwargs):
        _missing_dependencies_error("preprocessing_pipeline")
