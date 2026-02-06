import cv2
import os
import sys

# Ensure Python finds the filters folder
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from filters.edges import extract_edges
from filters.colors import apply_paint_effect

def process_images():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, '..', 'input')
    output_dir = os.path.join(script_dir, '..', 'output')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    valid_extensions = ('.jpg', '.jpeg', '.png')

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(valid_extensions):
            img = cv2.imread(os.path.join(input_dir, filename))
            if img is None: continue

            # 1. Get the "Painted" color version
            color_version = apply_paint_effect(img, k=8)

            # 2. Get the "Ink" edge version (Black and White)
            edges = extract_edges(img)

            # 3. COMBINE: Apply the black lines to the colored image
            # 'edges' is white (255) where it's clear and black (0) where there's a line.
            # We use it as a bitwise mask.
            final_cartoon = cv2.bitwise_and(color_version, color_version, mask=edges)

            # Save the final masterpiece
            output_path = os.path.join(output_dir, f"vector_{filename}")
            cv2.imwrite(output_path, final_cartoon)
            print(f"Masterpiece Created: vector_{filename}")

if __name__ == "__main__":
    process_images()