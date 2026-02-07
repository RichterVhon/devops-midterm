import cv2
import numpy as np

def extract_edges(image):
    """
    Converts a BGR image into a STRICT binary edge mask (0 and 255 only).
    """
    # 1. Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. Reduce noise
    blurred = cv2.medianBlur(gray, 7)

    # 3. Adaptive threshold for edge detection
    edges = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        9,
        2
    )

    # 4. Ensure strictly binary (just in case)
    edges = np.where(edges > 127, 255, 0).astype(np.uint8)

    return edges
