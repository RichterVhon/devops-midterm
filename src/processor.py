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

# 1. Capture the environment variable from the system
# We default to 'local' so your dashboard stays clean if you run it on your PC
current_env = os.getenv("APP_ENV", "local")

# 2. Initialize Sentry
# We remove the 'if' guard for the environment so we can actually see 
# the 'local' or 'ci' tags show up on the dashboard for testing.
if os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        environment=current_env, # This is what creates the dropdown in Sentry
        release=os.getenv("GITHUB_SHA", "v1.0.0"), # Best practice for Milestone 4
        traces_sample_rate=1.0,
        send_default_pii=True
    )
    print(f"Sentry initialized in [{current_env}] mode.")

def process_images():
    #division_by_zero = 1 / 0  # This will trigger an error to test Sentry integration
    # Define paths relative to this script
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

                base_name, _ = os.path.splitext(filename)

                # REQUIRED by tests (do NOT remove)
                mask_path = os.path.join(mask_debug_dir, f"mask_{base_name}.png")
                cv2.imwrite(mask_path, ink_mask)

                # 2. Paint effect
                painted_canvas = apply_paint_effect(img, k=8)

                # 3. Combine
                final_cartoon = cv2.bitwise_and(painted_canvas, painted_canvas, mask=ink_mask)

                # 4. Final output (the one you actually care about)
                output_filename = f"processed_{base_name}.png"
                output_path = os.path.join(output_dir, output_filename)
                cv2.imwrite(output_path, final_cartoon)

                print(f"Processed: {filename} -> {output_filename}")

            else:
                print(f"Warning: Could not read {filename}. Skipping.")

if __name__ == "__main__":
    process_images()