"""
Stormi

Stormi is a computational framework for probabilistic modeling of cellular dynamics,
particularly focusing on RNA transcription, protein expression, and gene regulation.

docs: https://stormi.celldynamix.net
source: https://github.com/celldynamics/stormi
PyPI package: https://pypi.org/project/stormi

Note: preprocessing functionality is available as an optional extra:
- Install it with: pip install stormi[preprocessing]
- Import from it with: from stormi.preprocessing import ...
"""

from importlib import metadata

from stormi import (
    guides,
    logging,
    models,
    plots,
    posterior,
    styles,
    train,
)
from stormi.main import main

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    __version__ = "unknown"

del metadata

__all__ = [
    "guides",
    "logging",
    "models",
    "plots",
    "posterior",
    "preprocessing",
    "styles",
    "train",
    "main",
]
