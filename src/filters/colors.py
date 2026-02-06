import cv2
import numpy as np

def apply_paint_effect(image, k=8):
    """
    Simplifies the image colors using K-Means and smooths it 
    with a Bilateral Filter for a 'painted' look.
    """
    # --- STEP A: K-MEANS CLUSTERING (Quantization) ---
    # Convert image to float32 for K-Means
    data = image.reshape((-1, 3))
    data = np.float32(data)

    # Define criteria and apply kmeans
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert back to uint8 and reshape to original image size
    center = np.uint8(center)
    quantized = center[label.flatten()]
    quantized = quantized.reshape((image.shape))

    # --- STEP B: BILATERAL FILTER (Smoothing) ---
    # d=9, sigmaColor=75, sigmaSpace=75 are standard for 'cartoon' smoothing
    painted = cv2.bilateralFilter(quantized, 9, 75, 75)
    
    return painted