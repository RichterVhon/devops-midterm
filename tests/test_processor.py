import os
import shutil
import cv2
import numpy as np
import pytest
from src.processor import run_processor

# The "Generic 3" assets you declared
TEST_IMAGES = ["test1.jpg", "test2.jpg", "test3.jpg"]

@pytest.mark.parametrize("image_name", TEST_IMAGES)
def test_full_cartoon_pipeline(image_name):
    """
    MATRIX TEST: Each image (1, 2, 3) must pass all logic gates.
    This script scales from simple plumbing to full filter validation.
    """
    # --- 1. SETUP ---
    asset_path = os.path.join("tests/assets", image_name)
    input_path = os.path.join("input", image_name)
    output_path = os.path.join("output", image_name)

    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    if not os.path.exists(asset_path):
        pytest.fail(f"Asset missing! Place {image_name} in tests/assets/")

    shutil.copy(asset_path, input_path)

    try:
        # --- 2. EXECUTION (The Plumbing) ---
        # This calls the main loop that the Lead Dev is building.
        run_processor()

        # --- 3. ASSERTION: I/O GATE ---
        # Basic plumbing check: Did the file actually move?
        assert os.path.exists(output_path), f"I/O Failure: {image_name} did not reach output/"
        
        original = cv2.imread(input_path)
        processed = cv2.imread(output_path)

        # --- 4. ASSERTION: CORRUPTION GATE ---
        assert processed is not None, f"Corruption: {image_name} is unreadable"
        assert original.shape == processed.shape, f"Geometry: {image_name} changed size"

        # --- 5. ASSERTION: THE "CHANGE" GATE ---
        # Proves the heater (filter) is 'on'.
        difference = cv2.absdiff(original, processed)
        assert np.any(difference > 0), f"Logic Error: {image_name} was not modified!"

        # =============================================================
        # 🚀 SCALE POINT: FEATURE VALIDATION HOOKS
        # As you add Milestone 2 (Edges) and Milestone 3 (Colors), 
        # the Tester will import and call their specific logic here.
        # =============================================================
        
        # EXAMPLE: Calling Milestone 2 (Edge Detection)
        # from tests.unit.test_edges import validate_ink_lines
        # assert validate_ink_lines(processed), "Edge filter failed quality check"

        # EXAMPLE: Calling Milestone 3 (Color Quantization)
        # from tests.unit.test_colors import validate_color_count
        # assert validate_color_count(processed), "Color filter failed to flatten palette"

    finally:
        # --- 6. TEARDOWN ---
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)