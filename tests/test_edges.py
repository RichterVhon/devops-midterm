import os
import cv2
import numpy as np
import pytest

# Import the actual filter we are validating
from src.filters.edges import extract_edges


# -------------------------------------------------
# CORE VALIDATOR (This will be used by other tests)
# -------------------------------------------------
def validate_ink_edges(edge_image, image_name="unknown"):
    """
    Ensures the edge output is a STRICT binary image.
    Allowed values: 0 and 255 only.
    """

    # Get unique pixel values
    unique_values = np.unique(edge_image)

    # Valid binary set
    allowed_values = {0, 255}

    # Convert numpy array to Python set
    pixel_set = set(unique_values.tolist())

    # Check if any invalid value exists
    invalid_values = pixel_set - allowed_values

    assert len(invalid_values) == 0, (
        f"Ink Filter Failure on {image_name}!\n"
        f"Invalid pixel values detected: {invalid_values}\n"
        f"Expected only 0 and 255."
    )


# -------------------------------------------------
# MATRIX CHECK (Run filter directly on assets)
# -------------------------------------------------
TEST_ASSETS = ["test1.png", "test2.png", "test3.png"]


@pytest.mark.parametrize("image_name", TEST_ASSETS)
def test_ink_filter_binary_output(image_name):
    asset_path = os.path.join("tests/assets", image_name)

    if not os.path.exists(asset_path):
        pytest.fail(f"Missing test asset: {image_name}")

    # Load original image
    img = cv2.imread(asset_path)

    assert img is not None, f"Could not load {image_name}"

    # Apply edge filter directly
    edges = extract_edges(img)

    # Validate mathematics
    validate_ink_edges(edges, image_name)