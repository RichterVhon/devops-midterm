import os
import shutil
import cv2
import numpy as np
import pytest
from src.processor import process_images as run_processor

TEST_IMAGES = ["test1.jpg", "test2.jpg", "test3.jpg"]

@pytest.mark.parametrize("image_name", TEST_IMAGES)
def test_full_cartoon_pipeline(image_name):
    # --- 1. SETUP ---
    asset_path = os.path.join("tests/assets", image_name)
    input_path = os.path.join("input", image_name)
    
    # FIXED: The test now looks for the 'processed_' prefix
    output_path = os.path.join("output", f"processed_{image_name}")

    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    if not os.path.exists(asset_path):
        pytest.fail(f"Asset missing! Place {image_name} in tests/assets/")

    shutil.copy(asset_path, input_path)

    try:
        # --- 2. EXECUTION ---
        run_processor()

        # --- 3. ASSERTION: I/O GATE ---
        assert os.path.exists(output_path), f"I/O Failure: {output_path} not found!"
        
        original = cv2.imread(input_path)
        processed = cv2.imread(output_path)

        # --- 4. ASSERTION: CORRUPTION GATE ---
        assert processed is not None, f"Corruption: {output_path} is unreadable"
        assert original.shape == processed.shape, f"Geometry: {image_name} changed size"

        # --- 5. ASSERTION: THE "CHANGE" GATE ---
        # Note: If the processor just copies the image, this will fail.
        # Once the Lead Dev adds the Edge filter, this will pass.
        difference = cv2.absdiff(original, processed)
        assert np.any(difference > 0), f"Logic Error: {image_name} was not modified!"

        # SCALE POINT: Milestone 2 (Edges) hooks will go here...

    finally:
        # --- 6. TEARDOWN ---
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)