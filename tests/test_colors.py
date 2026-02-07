import os
import cv2
import numpy as np
import pytest
from src.filters.colors import apply_paint_effect

ASSETS = "tests/assets"
TEST_IMAGES = ["test1.png", "test2.png", "test3.png"]

K = 8


def count_unique_colors(image):
    pixels = image.reshape(-1, 3)
    unique = np.unique(pixels, axis=0)
    return len(unique)


@pytest.mark.parametrize("image_name", TEST_IMAGES)
def test_palette_gate(image_name):

    path = os.path.join(ASSETS, image_name)
    original = cv2.imread(path)

    assert original is not None, f"Could not read {image_name}"

    quantized = apply_paint_effect(original, k=K, return_quantized=True)


    original_colors = count_unique_colors(original)
    quantized_colors = count_unique_colors(quantized)

    print("Original colors:", original_colors)
    print("Quantized colors:", quantized_colors)

    assert quantized_colors <= K
    assert quantized_colors < original_colors



@pytest.mark.parametrize("image_name", TEST_IMAGES)
def test_bilateral_gate(image_name):

    path = os.path.join(ASSETS, image_name)
    original = cv2.imread(path)

    painted = apply_paint_effect(original, k=K)

    assert original.shape == painted.shape
