import os
import shutil
import cv2
import numpy as np
import pytest
from src.processor import process_images as run_processor
from src.processor import process_images

# Import validator from test_edges
from tests.test_edges import validate_ink_edges
from tests.test_colors import palette_gate, bilateral_gate


TEST_IMAGES = ["test1.png", "test2.png", "test3.png"]

@pytest.mark.parametrize("image_name", TEST_IMAGES)
def test_full_cartoon_pipeline(image_name):
    # --- 1. SETUP ---
    asset_path = os.path.join("tests/assets", image_name)
    input_path = os.path.join("input", image_name)
    
    base_name, _ = os.path.splitext(image_name)
    output_dir = "output"
    processed_dir = os.path.join(output_dir, "processed")
    output_path = os.path.join(processed_dir, f"processed_{base_name}.png")

    mask_path = os.path.join(output_dir, ".debug_masks", f"mask_{base_name}.png")
    # Binary mask for validation

    os.makedirs("input", exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, ".debug_masks"), exist_ok=True)

    if not os.path.exists(asset_path):
        pytest.fail(f"Asset missing! Place {image_name} in tests/assets/")

    shutil.copy(asset_path, input_path)

    try:
        # --- 2. EXECUTION ---
        run_processor()
        
        # NEW: Give the OS a moment to finish writing the files to disk
        # This prevents the 'libpng Read Error'
        time.sleep(2)

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

        # --- 6. VALIDATE EDGE MASK MILESTONE 2---
        # Read the mask (strictly binary 0/255)
        mask_img = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        assert mask_img is not None, f"Mask could not be read for {image_name}"
        validate_ink_edges(mask_img, image_name)
        
        # --- 7. VALIDATE PAINT EFFECT MILESTONE 2---
        paint_path = os.path.join(output_dir, "paint", f"paint_{base_name}.png")
        paint_img = cv2.imread(paint_path)
        assert paint_img is not None, f"Paint image not readable: {paint_path}"
        
        palette_gate(paint_img)
        bilateral_gate(paint_img)
        

    finally:
        # --- 7. TEARDOWN ---
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        if os.path.exists(mask_path):
            os.remove(mask_path)

@pytest.mark.parametrize("image_name", TEST_IMAGES)
def test_full_cartoon_pipeline_tmp(image_name, tmp_path):
    # 1. Create temporary input/output folders
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    # 2. Load original image from assets
    asset_path = os.path.join("tests/assets", image_name)
    original = cv2.imread(asset_path)

    assert original is not None, f"Could not read {image_name}"

    # 3. Copy image into the input folder
    input_file = input_dir / image_name
    cv2.imwrite(str(input_file), original)

    # 4. RUN YOUR CARTOON MACHINE
    process_images(str(input_dir), str(output_dir))

    # 5. Check output file exists
    processed_dir = output_dir / "processed"
    output_file = processed_dir / f"processed_{image_name}"
    assert output_file.exists(), "Processed file was not created!"

    # 6. Read the result image
    result = cv2.imread(str(output_file))

    # 7. SAME SIZE CHECK
    assert result.shape == original.shape

    # 8. INK CHECK (dark lines exist)
    assert np.min(result) < 50

    # 9. PAINT CHECK (bright/color exists)
    assert np.max(result) > 200


def test_extreme_images(tmp_path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    # completely white image
    white = np.full((200, 200, 3), 255, dtype=np.uint8)

    # completely black image
    black = np.zeros((200, 200, 3), dtype=np.uint8)

    cv2.imwrite(str(input_dir / "white.jpg"), white)
    cv2.imwrite(str(input_dir / "black.jpg"), black)

    # pipeline should NOT crash
    process_images(str(input_dir), str(output_dir))

    # check outputs exist
    assert (output_dir / "processed" / "processed_white.jpg").exists()
    assert (output_dir / "processed" / "processed_black.jpg").exists()
