import cv2
import os
import sys

# Ensures Python treats the 'src' directory as the root for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# [x] Task: Import extract_edges and apply_paint_effect
from filters.edges import extract_edges
from filters.colors import apply_paint_effect

import sentry_sdk
import os

# The Handshake: Use the key provided by the YML
sentry_dsn = os.getenv("SENTRY_DSN")

if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        traces_sample_rate=1.0,
        # Only log if it's NOT a local test (optional logic)
        environment="production" if os.getenv("APP_ENV") == "production" else "development"
    )
    
def process_images():
    # Define paths relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, '..', 'input')
    output_dir = os.path.join(script_dir, '..', 'output')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    valid_extensions = ('.jpg', '.jpeg', '.png')

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(valid_extensions):
            input_path = os.path.join(input_dir, filename)
            
            # [x] Task: Ensure the final image is saved with the processed_ prefix
            output_filename = f"processed_{filename}"
            output_path = os.path.join(output_dir, output_filename)

            img = cv2.imread(input_path)

            if img is not None:
                # --- THE LOGIC SANDWICH ---
                
                # [x] 1. Generate the Ink Mask (Milestone 2)
                ink_mask = extract_edges(img)

                # [x] 2. Generate the Quantized/Smoothed Color Image (Milestone 3)
                painted_canvas = apply_paint_effect(img, k=8)

                # [x] 3. Use cv2.bitwise_and to overlay ink lines
                # This keeps the colors from 'painted_canvas' ONLY where 'ink_mask' is white.
                final_cartoon = cv2.bitwise_and(painted_canvas, painted_canvas, mask=ink_mask)

                # 4. Save the result
                cv2.imwrite(output_path, final_cartoon)
                print(f"Image Processed: {output_filename}")
            else:
                print(f"Warning: Could not read {filename}. Skipping.")

if __name__ == "__main__":
    process_images()