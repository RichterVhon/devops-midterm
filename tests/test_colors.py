import os
import cv2
import numpy as np
import pytest
from src.filters.colors import apply_paint_effect

ASSETS = "tests/assets"
TEST_IMAGES = ["test1.png", "test2.png", "test3.png"]
K = 8

# --- Reusable functions (no decorators) ---
def palette_gate(image, k=K):
    quantized = apply_paint_effect(image, k=k, return_quantized=True)
    original_colors = len(np.unique(image.reshape(-1, 3), axis=0))
    quantized_colors = len(np.unique(quantized.reshape(-1, 3), axis=0))
    assert quantized_colors <= k, "Too many colors in painted image"
    assert quantized_colors < original_colors, "Painting did not reduce colors"

def bilateral_gate(image, k=K):
    painted = apply_paint_effect(image, k=k)
    assert image.shape == painted.shape, "Bilateral filter changed image size"

# --- Pytest wrappers ---
@pytest.mark.parametrize("image_name", TEST_IMAGES)
def test_palette_gate(image_name):
    path = os.path.join(ASSETS, image_name)
    img = cv2.imread(path)
    assert img is not None, f"Could not read {image_name}"
    palette_gate(img)

@pytest.mark.parametrize("image_name", TEST_IMAGES)
def test_bilateral_gate(image_name):
    path = os.path.join(ASSETS, image_name)
    img = cv2.imread(path)
    assert img is not None, f"Could not read {image_name}"
    bilateral_gate(img)
