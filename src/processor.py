import cv2
import os
import sys
import time
import sentry_sdk

# Ensures Python treats the 'src' directory as the root for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)


from filters.edges import extract_edges
from filters.colors import apply_paint_effect


# -----------------------------
# ENVIRONMENT / SENTRY SETUP
# -----------------------------
if os.getenv("GITHUB_ACTIONS"):
    env = "ci"
elif os.getenv("APP_ENV") == "production":
    env = "production"
else:
    env = "local"

if env in ["ci", "production"] and os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        environment=env,
        traces_sample_rate=1.0
    )


# -----------------------------
# SINGLE IMAGE PIPELINE
# -----------------------------
def process_single_image(input_path, output_dir):
    """
    Processes ONE image safely.
    Used by watcher and batch mode.
    """

    filename = os.path.basename(input_path)
    base_name, ext = os.path.splitext(filename)

    # Output folders
    paint_dir = os.path.join(output_dir, "paint")
    processed_dir = os.path.join(output_dir, "processed")
    mask_debug_dir = os.path.join(output_dir, ".debug_masks")  # edges go here

    for d in [paint_dir, processed_dir, mask_debug_dir]:
        os.makedirs(d, exist_ok=True)

    # Retry logic (file may still be copying)
    img = None
    for _ in range(5):
        img = cv2.imread(input_path)
        if img is not None:
            break
        time.sleep(0.2)

    if img is None:
        print(f"❌ Failed to read image: {filename}")
        return

    # 1. Edge mask
    ink_mask = extract_edges(img)

    # Save debug mask / edges
    cv2.imwrite(
        os.path.join(mask_debug_dir, f"mask_{base_name}.png"),  # mask
        ink_mask
    )
    # 2. Paint effect
    painted_canvas = apply_paint_effect(img, k=8)
    cv2.imwrite(
        os.path.join(paint_dir, f"paint_{base_name}{ext}"),
        painted_canvas
    )

    # 3. Combine
    final_cartoon = cv2.bitwise_and(
        painted_canvas, painted_canvas, mask=ink_mask
    )

    # 4. Final output
    cv2.imwrite(
        os.path.join(processed_dir, f"processed_{base_name}{ext}"),
        final_cartoon
    )

def process_images(input_dir="input", output_dir="output"):
    """
    Batch process all images in the input folder using process_single_image.
    """
    if not os.path.exists(input_dir):
        print(f"Input directory {input_dir} does not exist!")
        return

    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            input_path = os.path.join(input_dir, filename)
            process_single_image(input_path, output_dir)