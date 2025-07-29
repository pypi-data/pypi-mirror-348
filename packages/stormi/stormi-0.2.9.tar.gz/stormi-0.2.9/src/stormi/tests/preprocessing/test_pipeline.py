"""Tests for the preprocessing pipeline module."""

import numpy as np
import pandas as pd

from stormi.preprocessing import (
    check_command_availability,
    preprocessing_pipeline,
)


def test_preprocessing_pipeline_full(dummy_anndata, dummy_files):
    """Test that the preprocessing pipeline runs successfully and produces expected outputs."""
    adata_rna, adata_atac = dummy_anndata
    main_dir = dummy_files

    # Check if bedtools is available - test will work with or without it
    has_bedtools = check_command_availability("bedtools")
    if not has_bedtools:
        print("bedtools not available - test will use fallback Python implementation")

    # Run the preprocessing pipeline
    result = preprocessing_pipeline(
        main_dir=main_dir,
        data_rna=adata_rna,
        data_atac=adata_atac,
        perform_clustering=False,
        chipseq_analysis=False,
        motif_match_pvalue_threshold=0.99,
        correlation_percentile=95.0,
    )

    # Check that the output files were created in the Generated directory.
    output_dir = main_dir / "Generated"
    rna_path = output_dir / "rna_processed.h5ad"
    atac_path = output_dir / "atac_processed.h5ad"

    # Both output files should exist regardless of bedtools availability
    assert rna_path.exists(), f"RNA processed file not found at {rna_path}"
    assert atac_path.exists(), f"ATAC processed file not found at {atac_path}"

    # Intersected peaks file should also exist whether bedtools is used or the fallback
    peaks_intersected_path = output_dir / "peaks_intersected.bed"
    assert peaks_intersected_path.exists(), (
        f"Intersected peaks file not found at {peaks_intersected_path}"
    )

    # the pipeline should return a DataFrame.
    assert isinstance(result, pd.DataFrame), (
        "Expected the pipeline to return a DataFrame from motif analysis."
    )
    # check that the DataFrame has the expected columns.
    expected_columns = {"peak_name", "Motif_name", "Matching_Score"}
    assert expected_columns.issubset(result.columns), (
        f"Result DataFrame is missing columns: {expected_columns - set(result.columns)}"
    )
    # Now check that the column data types are as expected.
    # For example, 'peak_name' and 'Motif_name' should be strings (object type) and 'Matching_Score' should be float.
    dtypes = result.dtypes
    assert dtypes["peak_name"] == object, (
        f"Expected 'peak_name' to be of type object, got {dtypes['peak_name']}"
    )
    assert dtypes["Motif_name"] == object, (
        f"Expected 'Motif_name' to be of type object, got {dtypes['Motif_name']}"
    )

    assert np.issubdtype(dtypes["Matching_Score"], float), (
        f"Expected 'Matching_Score' to be a float, got {dtypes['Matching_Score']}"
    )
