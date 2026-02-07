import os
import shutil
import cv2
import numpy as np
import pytest
from src.processor import process_images as run_processor

# Import validator from test_edges
from tests.test_edges import validate_ink_edges

TEST_IMAGES = ["test1.png", "test2.png", "test3.png"]

@pytest.mark.parametrize("image_name", TEST_IMAGES)
def test_full_cartoon_pipeline(image_name):
    # --- 1. SETUP ---
    asset_path = os.path.join("tests/assets", image_name)
    input_path = os.path.join("input", image_name)
    
    base_name, _ = os.path.splitext(image_name)
    output_dir = "output"
    output_path = os.path.join(output_dir, f"processed_{base_name}.png")
    mask_path = os.path.join(output_dir, ".debug_masks", f"mask_{base_name}.png")  # Binary mask for validation

    os.makedirs("input", exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, ".debug_masks"), exist_ok=True)

    if not os.path.exists(asset_path):
        pytest.fail(f"Asset missing! Place {image_name} in tests/assets/")

    shutil.copy(asset_path, input_path)

    try:
        # --- 2. EXECUTION ---
        run_processor()

        # --- 3. ASSERTION: I/O GATE ---
        assert os.path.exists(output_path), f"I/O Failure: {output_path} not found!"
        assert os.path.exists(mask_path), f"I/O Failure: {mask_path} not found!"

        original = cv2.imread(input_path)
        processed_cartoon = cv2.imread(output_path)

        # --- 4. ASSERTION: CORRUPTION GATE ---
        assert processed_cartoon is not None, f"Corruption: {output_path} is unreadable"
        assert original.shape == processed_cartoon.shape, f"Geometry: {image_name} changed size"

        # --- 5. ASSERTION: THE "CHANGE" GATE ---
        difference = cv2.absdiff(original, processed_cartoon)
        assert np.any(difference > 0), f"Logic Error: {image_name} was not modified!"

        # --- 6. VALIDATE EDGE MASK ---
        # Read the mask (strictly binary 0/255)
        mask_img = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        assert mask_img is not None, f"Mask could not be read for {image_name}"
        validate_ink_edges(mask_img, image_name)

    finally:
        # --- 7. TEARDOWN ---
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        if os.path.exists(mask_path):
            os.remove(mask_path)
