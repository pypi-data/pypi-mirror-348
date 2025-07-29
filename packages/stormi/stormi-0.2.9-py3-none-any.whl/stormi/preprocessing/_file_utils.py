"""File operation utilities for downloading and manipulating reference files."""

import logging
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Tuple

from beartype import beartype

logger = logging.getLogger(__name__)


@beartype
def create_dir_if_not_exists(directory: Path) -> None:
    """Create the directory if it does not exist.

    Args:
        directory: Path to directory to create.
    """
    if not directory.exists():
        logger.info(f"Creating directory: {directory}")
        directory.mkdir(parents=True, exist_ok=True)


@beartype
def download_file(url: str, out_path: Path) -> None:
    """Download a file from URL to the specified path using wget.

    Args:
        url: The URL to download from.
        out_path: The local file path to save the downloaded file.
    """
    if out_path.exists():
        logger.info(f"File already exists: {out_path}. Skipping download.")
        return
    cmd = f"wget --no-verbose -O {out_path} {url}"
    logger.info(f"Downloading {url} -> {out_path}")
    subprocess.run(cmd, shell=True, check=True)


@beartype
def unzip_gz(file_path: Path, remove_input: bool = False) -> None:
    """Gzip-decompress a file.

    Args:
        file_path: Path to the .gz file to decompress.
        remove_input: If True, deletes the original .gz file after decompression.
    """
    cmd = f"gzip -d {file_path}"
    logger.info(f"Decompressing {file_path}")
    subprocess.run(cmd, shell=True, check=True)
    if remove_input:
        gz_file = file_path
        if gz_file.exists():
            gz_file.unlink()


@beartype
def resolve_genome_urls(
    species: str,
    assembly: str,
    gtf_url: Optional[str],
    chrom_sizes_url: Optional[str],
    fasta_url: Optional[str],
) -> Tuple[str, str, str]:
    """Resolve URLs for genome reference files.

    Determines which URLs to use for GTF, chrom.sizes, and FASTA files based on:
    1) species & assembly (e.g. "mouse", "mm10" or "human", "hg38")
    2) user-provided overrides in config

    Args:
        species: The organism species (e.g., "mouse", "human").
        assembly: The genome assembly version (e.g., "mm10", "hg38").
        gtf_url: Optional user-provided URL for GTF annotation file.
        chrom_sizes_url: Optional user-provided URL for chromosome sizes file.
        fasta_url: Optional user-provided URL for genome FASTA file.

    Returns:
        Tuple containing (gtf_url, chrom_sizes_url, fasta_url).

    Raises:
        ValueError: If URLs cannot be resolved for unknown assembly/species.
    """
    # If user provided them in config, we override. If not, we set defaults for known combos.
    final_gtf_url = gtf_url
    final_chrom_sizes_url = chrom_sizes_url
    final_fasta_url = fasta_url

    # Known defaults for mouse mm10
    if species.lower() == "mouse" and assembly.lower() == "mm10":
        if final_gtf_url is None:
            final_gtf_url = (
                "https://ftp.ebi.ac.uk/pub/databases/gencode/"
                "Gencode_mouse/release_M18/gencode.vM18.basic.annotation.gtf.gz"
            )
        if final_chrom_sizes_url is None:
            final_chrom_sizes_url = "https://hgdownload.cse.ucsc.edu/goldenpath/mm10/bigZips/mm10.chrom.sizes"
        if final_fasta_url is None:
            final_fasta_url = (
                "https://hgdownload.soe.ucsc.edu/goldenPath/mm10/bigZips/mm10.fa.gz"
            )

    # Known defaults for human hg38
    elif species.lower() == "human" and assembly.lower() == "hg38":
        if final_gtf_url is None:
            final_gtf_url = (
                "https://ftp.ebi.ac.uk/pub/databases/gencode/"
                "Gencode_human/release_47/gencode.v47.primary_assembly.basic.annotation.gtf.gz"
            )
        if final_chrom_sizes_url is None:
            final_chrom_sizes_url = "https://hgdownload.cse.ucsc.edu/goldenpath/hg38/bigZips/hg38.chrom.sizes"
        if final_fasta_url is None:
            final_fasta_url = (
                "https://hgdownload.cse.ucsc.edu/goldenpath/hg38/bigZips/hg38.fa.gz"
            )

    else:
        # Unknown assembly => user must provide or raise an error if any is None
        if (
            final_gtf_url is None
            or final_chrom_sizes_url is None
            or final_fasta_url is None
        ):
            raise ValueError(
                f"Unknown assembly '{assembly}' for species='{species}'. "
                "Please provide gtf_url, chrom_sizes_url, and fasta_url in config."
            )

    return (final_gtf_url, final_chrom_sizes_url, final_fasta_url)


@beartype
def download_genome_references(
    genome_dir: Path,
    species: str,
    assembly: str,
    gtf_url: Optional[str] = None,
    chrom_sizes_url: Optional[str] = None,
    fasta_url: Optional[str] = None,
) -> None:
    """Download genome reference files for a specified species and assembly.

    Downloads GTF, chromosome sizes, and FASTA files if not already present locally.

    Args:
        genome_dir: Directory to save the downloaded files.
        species: The organism species (e.g., "mouse", "human").
        assembly: The genome assembly version (e.g., "mm10", "hg38").
        gtf_url: Optional URL for the GTF annotation file.
        chrom_sizes_url: Optional URL for the chromosome sizes file.
        fasta_url: Optional URL for the genome FASTA file.
    """
    genome_dir.mkdir(parents=True, exist_ok=True)

    # 1) Resolve the final URLs based on species/assembly + user overrides
    final_gtf_url, final_chrom_sizes_url, final_fasta_url = resolve_genome_urls(
        species, assembly, gtf_url, chrom_sizes_url, fasta_url
    )
    logger.info(
        f"Using genome references for species='{species}', assembly='{assembly}'.\n"
        f"GTF: {final_gtf_url}\n"
        f"Chrom.sizes: {final_chrom_sizes_url}\n"
        f"FASTA: {final_fasta_url}"
    )

    # Decide on local filenames
    gtf_gz = genome_dir / f"{species}_annotation.gtf.gz"
    gtf_final = genome_dir / f"{species}_annotation.gtf"
    chrom_sizes_path = genome_dir / f"{species}_{assembly}.chrom.sizes"
    fasta_gz = genome_dir / f"{species}_{assembly}.fa.gz"
    fasta_final = genome_dir / f"{species}_{assembly}.fa"

    # 2) GTF
    if not gtf_final.exists():
        download_file(final_gtf_url, gtf_gz)
        unzip_gz(gtf_gz, remove_input=True)

    # 3) chrom sizes
    if not chrom_sizes_path.exists():
        download_file(final_chrom_sizes_url, chrom_sizes_path)

    # 4) FASTA
    if not fasta_final.exists():
        download_file(final_fasta_url, fasta_gz)
        unzip_gz(fasta_gz, remove_input=True)

    logger.info(f"Reference files are ready in {genome_dir}")


@beartype
def check_command_availability(command: str) -> bool:
    """Check if a command is available in the system PATH.

    Args:
        command: The command name to check.

    Returns:
        True if the command is available, False otherwise.
    """
    return shutil.which(command) is not None
