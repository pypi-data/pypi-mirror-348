"""Configuration for preprocessing tests with proper handling of missing dependencies."""

import importlib
import logging
from pathlib import Path

import pytest

logger = logging.getLogger(__name__)

# Check if preprocessing dependencies are available
MISSING_DEPENDENCIES = []


def _check_dependency(module_name):
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        MISSING_DEPENDENCIES.append(module_name)
        return False


# Check key preprocessing dependencies
HAS_PREPROCESSING = (
    _check_dependency("pyranges")
    and _check_dependency("pybiomart")
    and _check_dependency("tangermeme")
    and _check_dependency("gtfparse")
)


# Custom pytest collection hook to skip preprocessing tests when dependencies are missing
def pytest_collection_modifyitems(config, items):
    """Skip preprocessing tests when dependencies are missing."""
    if not HAS_PREPROCESSING:
        skip_preprocessing = pytest.mark.skip(
            reason=f"Preprocessing dependencies not installed: {', '.join(MISSING_DEPENDENCIES)}. "
            "Install with: pip install stormi[preprocessing]"
        )
        for item in items:
            # Skip any test modules in the preprocessing directory
            if str(item.fspath).find(str(Path("tests") / "preprocessing")) != -1:
                item.add_marker(skip_preprocessing)

        # Log a clear message about missing dependencies
        if MISSING_DEPENDENCIES:
            deps_str = ", ".join(MISSING_DEPENDENCIES)
            logger.warning(
                f"Skipping preprocessing tests because required dependencies are missing: {deps_str}. "
                "Install with: pip install stormi[preprocessing]"
            )


import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from anndata import AnnData


@pytest.fixture
def dummy_anndata():
    """
    Create dummy RNA and ATAC AnnData objects for testing.

    Returns:
        tuple: A tuple containing (adata_rna, adata_atac) AnnData objects.
    """
    # ---- Create dummy RNA AnnData object ----
    # 10 cells and 10 genes
    cell_ids = [
        "cell_1",
        "cell_2",
        "cell_3",
        "cell_4",
        "cell_5",
        "cell_6",
        "cell_7",
        "cell_8",
        "cell_9",
        "cell_10",
    ]

    gene_names = [
        "TF1",
        "TF2",
        "Gene3",
        "Gene4",
        "Gene5",
        "Gene6",
        "Gene7",
        "Gene8",
        "Gene9",
        "Gene10",
    ]

    rna_data = np.random.rand(10, 10)
    rna_obs = pd.DataFrame(index=cell_ids)
    rna_var = pd.DataFrame(index=gene_names)
    adata_rna = AnnData(X=rna_data, obs=rna_obs, var=rna_var)

    # ---- Create dummy ATAC AnnData object ----
    peak_names = [
        "chr1:110-290",
        "chr1:310-390",
        "chr1:3000-3100",
        "chr1:4000-4100",
        "chr1:5000-5100",
        "chr1:6000-6100",
        "chr1:7000-7100",
        "chr1:8000-8100",
        "chr1:9000-9100",
        "chr1:10000-10100",
    ]

    atac_data = np.random.randint(0, 5, size=(10, 10))
    atac_obs = pd.DataFrame(index=cell_ids)
    atac_var = pd.DataFrame(index=peak_names)
    adata_atac = AnnData(X=atac_data, obs=atac_obs, var=atac_var)

    return adata_rna, adata_atac


@pytest.fixture
def dummy_files(tmp_path):
    """
    Create a dummy file structure with necessary files for testing.

    Args:
        tmp_path: Pytest fixture that provides a temporary directory.

    Returns:
        Path: Path to the main directory containing the test files.
    """
    # Create a main directory
    main_dir = tmp_path / "main_dir"
    main_dir.mkdir()

    # Create subdirectories as expected by the pipeline
    prepared_dir = main_dir / "Prepared"
    prepared_dir.mkdir()
    generated_dir = main_dir / "Generated"
    generated_dir.mkdir()

    # Create a dummy GTF file with gene information
    gtf_lines = [
        'chr1\tDummySource\tgene\t100\t1500\t.\t+\t.\tgene_id "TF1"; gene_name "TF1"; gene_type "protein_coding";',
        'chr1\tDummySource\tgene\t2000\t2500\t.\t+\t.\tgene_id "TF2"; gene_name "TF2"; gene_type "protein_coding";',
        'chr1\tDummySource\tgene\t3000\t3500\t.\t+\t.\tgene_id "Gene3"; gene_name "mt-Gene3"; gene_type "protein_coding";',
        'chr1\tDummySource\tgene\t4000\t4500\t.\t+\t.\tgene_id "Gene4"; gene_name "Gene4"; gene_type "protein_coding";',
        'chr1\tDummySource\tgene\t5000\t5500\t.\t+\t.\tgene_id "Gene5"; gene_name "Gene5"; gene_type "protein_coding";',
        'chr1\tDummySource\tgene\t6000\t6500\t.\t+\t.\tgene_id "Gene6"; gene_name "Gene6"; gene_type "protein_coding";',
        'chr1\tDummySource\tgene\t7000\t7500\t.\t+\t.\tgene_id "Gene7"; gene_name "Gene7"; gene_type "protein_coding";',
        'chr1\tDummySource\tgene\t8000\t8500\t.\t+\t.\tgene_id "Gene8"; gene_name "Gene8"; gene_type "protein_coding";',
        'chr1\tDummySource\tgene\t9000\t9500\t.\t+\t.\tgene_id "Gene9"; gene_name "Gene9"; gene_type "protein_coding";',
        'chr1\tDummySource\tgene\t10000\t10500\t.\t+\t.\tgene_id "Gene10"; gene_name "Gene10"; gene_type "non_prot_coding";',
    ]

    gtf_file = prepared_dir / "mouse_annotation.gtf"
    gtf_file.write_text("\n".join(gtf_lines))

    # Create a dummy motif file with motifs for TF1 and TF2
    meme_file = prepared_dir / "cisbp_mouse.meme"
    motif_data = (
        "MOTIF dummy TF1\n\n"
        "letter-probability matrix: alength= 4 w= 10 nsites= 1 E= 0\n"
        "  0.220377        0.335405        0.102037        0.342181\n"
        "  0.111784        0.193750        0.669524        0.024942\n"
        "  0.009553        0.989147        0.000370        0.000929\n"
        "  0.000437        0.891193        0.000324        0.108046\n"
        "  0.046223        0.377462        0.191229        0.385087\n"
        "  0.132612        0.336106        0.329451        0.201830\n"
        "  0.430307        0.248265        0.229178        0.092250\n"
        "  0.301624        0.024759        0.651437        0.022180\n"
        "  0.055101        0.000431        0.943092        0.001376\n"
        "  0.095237        0.349453        0.435445        0.119865\n\n"
        "URL http://dummy-url.com/TF1\n\n"
        "MOTIF dummy TF2\n\n"
        "letter-probability matrix: alength= 4 w= 10 nsites= 1 E= 0\n"
        "  0.000019        0.999823        0.000038        0.000120\n"
        "  0.000091        0.899183        0.000093        0.100634\n"
        "  0.023042        0.234469        0.177208        0.565281\n"
        "  0.107618        0.390953        0.394882        0.106547\n"
        "  0.537857        0.155647        0.286458        0.020037\n"
        "  0.051649        0.000023        0.948115        0.000213\n"
        "  0.000014        0.000011        0.999930        0.000045\n"
        "  0.000011        0.667311        0.331377        0.001301\n"
        "  0.201422        0.246017        0.349115        0.203446\n"
        "  0.598826        0.108307        0.129667        0.163199\n\n"
        "URL http://dummy-url.com/TF2\n"
    )
    meme_file.write_text(motif_data)

    # Create a dummy FASTA file
    fasta_file = prepared_dir / "mouse_mm10.fa"
    sequence = "ATC" * 600
    with open(fasta_file, "w") as f:
        f.write(">chr1\n")
        for i in range(0, 600, 53):
            f.write(sequence[i : i + 53] + "\n")

    # Create a dummy chrom.sizes file for mouse_mm10
    chrom_sizes_file = prepared_dir / "mouse_mm10.chrom.sizes"
    chrom_sizes_file.write_text("chr1\t1000000\nchr2\t2000000\n")

    return main_dir
