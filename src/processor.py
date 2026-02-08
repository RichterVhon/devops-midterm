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

import os
import sentry_sdk

# Determine where we are running
if os.getenv("GITHUB_ACTIONS"):
    env = "ci"
elif os.getenv("APP_ENV") == "production":
    env = "production"
else:
    env = "local"

# Only "Turn on" Sentry for CI and Production
if env in ["ci", "production"] and os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        environment=env,  # This tags the error so you can filter the dashboard
        traces_sample_rate=1.0
    )

def process_images(input_dir=None, output_dir=None): 
    #division_by_zero = 1 / 0  # This will trigger an error to test Sentry integration
    # Define paths relative to this script
# Define default folders if none are provided
    if input_dir is None or output_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_dir = os.path.join(script_dir, '..', 'input')
        output_dir = os.path.join(script_dir, '..', 'output')

    os.makedirs(output_dir, exist_ok=True)
    mask_debug_dir = os.path.join(output_dir, ".debug_masks")
    os.makedirs(mask_debug_dir, exist_ok=True)

    
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

                # 1. Edge mask
                ink_mask = extract_edges(img)

                base_name, ext = os.path.splitext(filename)

                # REQUIRED by tests (do NOT remove)
                mask_path = os.path.join(mask_debug_dir, f"mask_{base_name}.png")
                cv2.imwrite(mask_path, ink_mask)

                # 2. Paint effect
                painted_canvas = apply_paint_effect(img, k=8)

                # 3. Combine
                final_cartoon = cv2.bitwise_and(painted_canvas, painted_canvas, mask=ink_mask)

                # 4. Final output (the one you actually care about)
                output_filename = f"processed_{base_name}{ext}"
                output_path = os.path.join(output_dir, output_filename)
                cv2.imwrite(output_path, final_cartoon)

                print(f"Processed: {filename} -> {output_filename}")

            else:
                print(f"Warning: Could not read {filename}. Skipping.")

if __name__ == "__main__":
    process_images()