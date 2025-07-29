"""Tests for file utility functions in the preprocessing subpackage."""

import os
import shutil
from pathlib import Path

import pytest

from stormi.preprocessing._file_utils import (
    check_command_availability,
    create_dir_if_not_exists,
    download_file,
    resolve_genome_urls,
)


def test_create_dir_if_not_exists(tmp_path):
    """Test that a directory is created if it doesn't exist."""
    test_dir = tmp_path / "test_dir"
    assert not test_dir.exists()

    # Call the function
    create_dir_if_not_exists(test_dir)

    # Verify the directory was created
    assert test_dir.exists()
    assert test_dir.is_dir()

    # Call again to test idempotency
    create_dir_if_not_exists(test_dir)
    assert test_dir.exists()


def test_check_command_availability():
    """Test that the command availability check works correctly."""
    # Test a command that should definitely be available
    assert check_command_availability("python") is True

    # Test a command that definitely shouldn't exist
    assert check_command_availability("this_command_does_not_exist_12345") is False


def test_resolve_genome_urls():
    """Test resolving genome URLs for different species and assemblies."""
    # Test mouse mm10 defaults
    gtf_url, chrom_sizes_url, fasta_url = resolve_genome_urls(
        "mouse", "mm10", None, None, None
    )
    assert "gencode" in gtf_url.lower()
    assert "mouse" in gtf_url.lower()
    assert "mm10" in chrom_sizes_url.lower()
    assert "mm10" in fasta_url.lower()

    # Test human hg38 defaults
    gtf_url, chrom_sizes_url, fasta_url = resolve_genome_urls(
        "human", "hg38", None, None, None
    )
    assert "gencode" in gtf_url.lower()
    assert "human" in gtf_url.lower()
    assert "hg38" in chrom_sizes_url.lower()
    assert "hg38" in fasta_url.lower()

    # Test user-provided URLs take precedence
    custom_gtf = "https://example.com/custom.gtf.gz"
    custom_chrom = "https://example.com/custom.chrom.sizes"
    custom_fasta = "https://example.com/custom.fa.gz"

    gtf_url, chrom_sizes_url, fasta_url = resolve_genome_urls(
        "mouse", "mm10", custom_gtf, custom_chrom, custom_fasta
    )
    assert gtf_url == custom_gtf
    assert chrom_sizes_url == custom_chrom
    assert fasta_url == custom_fasta

    # Test error for unknown assembly/species
    with pytest.raises(ValueError):
        resolve_genome_urls("unknown", "unknown", None, None, None)


def test_download_file(tmp_path, monkeypatch):
    """Test the download_file function with a mock subprocess call."""

    # Mock the subprocess.run function
    def mock_run(*args, **kwargs):
        class MockResult:
            returncode = 0

        # Create an empty file to simulate download
        with open(args[0].split(" ")[3], "w") as f:
            f.write("mock content")
        return MockResult()

    monkeypatch.setattr("subprocess.run", mock_run)

    # Test downloading a file
    out_path = tmp_path / "test_file.txt"
    download_file("https://example.com/test.txt", out_path)

    # Verify the file exists
    assert out_path.exists()
    assert out_path.read_text() == "mock content"

    # Test that download is skipped if file exists
    with monkeypatch.context() as m:
        # Set up a mock that would fail if called
        def failing_mock(*args, **kwargs):
            raise RuntimeError("This should not be called")

        m.setattr("subprocess.run", failing_mock)

        # Call again - should skip download
        download_file("https://example.com/test.txt", out_path)
        # If we get here, the download was skipped as expected
