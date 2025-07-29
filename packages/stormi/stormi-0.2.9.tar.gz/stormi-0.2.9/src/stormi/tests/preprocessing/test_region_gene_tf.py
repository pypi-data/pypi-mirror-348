"""Tests for region-gene-TF relationship functions in the preprocessing subpackage."""

import numpy as np
import pytest

# Import from the main preprocessing module instead of directly from submodule
# This ensures our conftest.py skip mechanism works properly
try:
    from stormi.preprocessing import rhg_to_rh_indexing
except ImportError:
    pytest.skip("Preprocessing dependencies not installed", allow_module_level=True)


def test_rhg_to_rh_indexing():
    """
    Test the rhg_to_rh_indexing function which maps region-TF-gene triplets to indices in region-TF pairs.

    This test ensures that:
    1. The function correctly maps triplets to their corresponding pair indices
    2. The mapped indices can be used to retrieve the original region-TF pairs
    3. The function raises ValueError when triplets contain pairs not found in the region-TF pairs
    """
    # Test data
    region_tf_gene_triplets = np.array(
        [
            [1, 3000, 1803],
            [1, 3027, 1803],
            [1, 3127, 1803],
            [10, 3000, 55],
            [63, 3000, 2500],
            [22239, 3298, 235],
            [43689, 3298, 3085],
            [43689, 3298, 1660],
            [49982, 3299, 1000],
            [49999, 3299, 2000],
        ]
    )

    region_tf_pairs = np.array(
        [
            [1, 3000],
            [10, 3000],
            [63, 3000],
            [1, 3027],
            [1, 3127],
            [22239, 3298],
            [32434, 3298],
            [43689, 3298],
            [49982, 3299],
            [49998, 3299],
            [49999, 3299],
        ]
    )

    region_tf_indices = rhg_to_rh_indexing(region_tf_gene_triplets, region_tf_pairs)

    # Indexing region_tf_pairs with region_tf_indices should retrieve [R, H] pairs
    # in the same order as region_tf_gene_triplets
    assert np.all(
        region_tf_pairs[region_tf_indices, :] == region_tf_gene_triplets[:, :2]
    )

    # Test ValueError case when a region-TF pair in triplets doesn't exist in region_tf_pairs
    invalid_triplets = np.array(
        [
            [1, 3000, 1803],
            [
                22239,
                3198,
                235,
            ],  # This pair [22239, 3198] doesn't exist in region_tf_pairs
        ]
    )

    with pytest.raises(ValueError, match="Unmapped entries in region_tf_gene_triplets"):
        rhg_to_rh_indexing(invalid_triplets, region_tf_pairs)
