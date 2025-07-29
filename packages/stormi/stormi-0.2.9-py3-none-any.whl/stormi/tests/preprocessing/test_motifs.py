"""Tests for the _motifs module."""

from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

from stormi.preprocessing._motifs import (
    compute_in_silico_chipseq,
    compute_motif_scores,
)


@pytest.fixture
def mock_atac_matrix():
    """Create a mock ATAC matrix (cells x peaks)."""
    n_cells, n_peaks = 10, 5
    # Simulate some counts, ensure variability
    matrix = np.random.poisson(1, size=(n_cells, n_peaks)).astype(float)
    matrix[matrix > 5] = 5  # Cap counts
    # Ensure some zeros
    zero_indices = np.random.choice(
        n_cells * n_peaks, size=int(0.2 * n_cells * n_peaks), replace=False
    )
    matrix.flat[zero_indices] = 0
    # Add some noise
    matrix += np.random.normal(0, 0.1, size=matrix.shape)
    matrix = np.clip(matrix, 0, None)  # Ensure non-negative
    # Ensure some std dev for z-scoring
    col_std = matrix.std(axis=0)
    for j in range(n_peaks):
        if col_std[j] < 1e-6:
            matrix[:, j] += np.random.normal(0, 0.5, size=n_cells)
    matrix = np.clip(matrix, 0, None)  # Ensure non-negative again
    return matrix


@pytest.fixture
def mock_rna_matrix(mock_df_motif):  # Depends on mock_df_motif for TF names
    """Create a mock RNA matrix (cells x TFs)."""
    n_cells = 10  # Match mock_atac_matrix
    tf_names = mock_df_motif.columns.tolist()
    n_tfs = len(tf_names)
    # Simulate expression, ensure variability
    matrix = np.random.gamma(2, 1, size=(n_cells, n_tfs)).astype(float)
    # Ensure some zeros
    zero_indices = np.random.choice(
        n_cells * n_tfs, size=int(0.1 * n_cells * n_tfs), replace=False
    )
    matrix.flat[zero_indices] = 0
    # Ensure some std dev for z-scoring
    col_std = matrix.std(axis=0)
    for j in range(n_tfs):
        if col_std[j] < 1e-6:
            matrix[:, j] += np.random.normal(0, 0.5, size=n_cells)
    matrix = np.clip(matrix, 0, None)  # Ensure non-negative

    return matrix


@pytest.fixture
def mock_df_motif():
    """Create mock motif scores DataFrame (peaks x TFs)."""
    peaks = [f"peak{i}" for i in range(5)]
    tfs = ["TF1", "TF2", "TF3"]
    # Simulate scores after MinMax scaling (0 to 1)
    scores = np.random.rand(len(peaks), len(tfs))
    return pd.DataFrame(scores, index=peaks, columns=tfs)


@pytest.fixture
def mock_pwms_sub():
    """Create a mock pwms_sub dictionary."""
    # This would typically contain PWM objects, but for mocking we can use placeholders
    return {
        "MOTIF TF1": MagicMock(),
        "MOTIF TF2": MagicMock(),
        "MOTIF TF3": MagicMock(),
    }


@pytest.fixture
def mock_key_to_tf():
    """Create a mock key_to_tf dictionary."""
    return {
        "MOTIF TF1": "TF1",
        "MOTIF TF2": "TF2",
        "MOTIF TF3": "TF3",
    }


def test_compute_motif_scores(tmp_path, mock_pwms_sub, mock_key_to_tf):
    """Test compute_motif_scores function with minimal mocking.

    Creates a real BED file and mocks only the tangermeme functions.
    """
    # Set up test parameters
    n_peaks = 5
    n_tfs = 3
    peak_names = [f"peak{i}" for i in range(n_peaks)]
    tf_names = [f"TF{i + 1}" for i in range(n_tfs)]

    # Create a real BED file
    bed_file = tmp_path / "test.bed"
    with open(bed_file, "w") as f:
        for i, name in enumerate(peak_names):
            f.write(f"chr1\t{i * 1000}\t{i * 1000 + 200}\t{name}\n")

    # Create an empty mock FASTA file
    fasta_file = tmp_path / "test.fa"
    fasta_file.touch()

    # Create patch context managers
    extract_loci_patch = patch("tangermeme.io.extract_loci")
    fimo_patch = patch("tangermeme.tools.fimo.fimo")

    # Start patches
    with extract_loci_patch as mock_extract_loci, fimo_patch as mock_fimo:
        # Mock extract_loci: return a mock with float() method
        mock_sequence_data = MagicMock()
        mock_sequence_data.float.return_value = np.random.rand(n_peaks, 100)
        mock_extract_loci.return_value = mock_sequence_data

        # Mock fimo: return a list of DataFrames with hits
        mock_fimo_hits = []
        for motif_key, tf_name in mock_key_to_tf.items():
            # Create hits for about half the peaks for each TF
            hit_indices = np.random.choice(range(n_peaks), n_peaks // 2, replace=False)
            hit_data = {
                "motif_name": [motif_key] * len(hit_indices),
                "sequence_name": hit_indices,
                "score": np.random.rand(len(hit_indices)) * 10,
            }
            mock_fimo_hits.append(pd.DataFrame(hit_data))
        mock_fimo.return_value = mock_fimo_hits

        # Call the function
        result_df = compute_motif_scores(
            bed_file=bed_file,
            fasta_file=fasta_file,
            pwms_sub=mock_pwms_sub,
            key_to_tf=mock_key_to_tf,
            n_peaks=n_peaks,
            window=100,
            threshold=1e-4,
            batch_size_Fimo_scan=100,
        )

        # Verify result
        assert isinstance(result_df, pd.DataFrame)
        assert result_df.shape == (n_peaks, n_tfs)
        assert list(result_df.index) == peak_names
        assert set(result_df.columns) == set(tf_names)

        # Check scores are in range [0, 1] due to MinMaxScaler
        assert result_df.values.min() >= 0.0
        assert result_df.values.max() <= 1.0

        # Verify mocks were called appropriately
        mock_extract_loci.assert_called_once()
        mock_fimo.assert_called_once()


def test_compute_in_silico_chipseq(mock_df_motif, mock_atac_matrix, mock_rna_matrix):
    """Test compute_in_silico_chipseq function."""
    correlation_percentile = 95.0
    n_bg_peaks_for_corr = 3  # Use small value to ensure it doesn't exceed n_peaks
    n_peaks, n_tfs = mock_df_motif.shape
    n_cells = mock_atac_matrix.shape[0]

    # Ensure matrix dimensions align
    assert mock_atac_matrix.shape == (n_cells, n_peaks)
    assert mock_rna_matrix.shape == (n_cells, n_tfs)
    assert list(mock_df_motif.columns) == [
        f"TF{i + 1}" for i in range(n_tfs)
    ]  # Check TF order if needed

    result_df = compute_in_silico_chipseq(
        df_motif=mock_df_motif,
        atac_matrix=mock_atac_matrix,
        rna_matrix=mock_rna_matrix,
        correlation_percentile=correlation_percentile,
        n_bg_peaks_for_corr=n_bg_peaks_for_corr,
    )

    assert isinstance(result_df, pd.DataFrame)

    # Check columns (long format expected)
    expected_columns = ["peak_name", "Motif_name", "Matching_Score"]
    assert all(col in result_df.columns for col in expected_columns)
    assert len(result_df.columns) == len(expected_columns)

    # Check data types
    assert pd.api.types.is_string_dtype(result_df["peak_name"])
    assert pd.api.types.is_string_dtype(result_df["Motif_name"])
    assert pd.api.types.is_numeric_dtype(result_df["Matching_Score"])

    # Check score range (scaled between -1 and 1)
    if not result_df.empty:
        assert (
            result_df["Matching_Score"].min() >= -1.0 - 1e-9
        )  # Allow for float precision
        assert (
            result_df["Matching_Score"].max() <= 1.0 + 1e-9
        )  # Allow for float precision

    # Check that peak names and motif names come from the input df_motif
    if not result_df.empty:
        assert set(result_df["peak_name"]).issubset(set(mock_df_motif.index))
        assert set(result_df["Motif_name"]).issubset(set(mock_df_motif.columns))

    # Check that only non-zero scores are returned
    assert not np.any(np.isclose(result_df["Matching_Score"], 0))
