import cv2

def extract_edges(image):
    """
    Converts a standard BGR image into a binary (Black & White) edge mask.
    """
    # 1. Grayscale: Simplifies the data from 3 channels to 1
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 2. Median Blur: Reduces noise (kernel size 7 is great for thick lines)
    # The kernel must be an odd number.
    blurred = cv2.medianBlur(gray, 7)
    
    # 3. Adaptive Thresholding: Creates the "Ink" look
    # blockSize 9 and C 2 are common defaults; adjust for thicker/thinner lines
    edges = cv2.adaptiveThreshold(
        blurred, 
        255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 
        9, 
        2
    )
    
    return edges