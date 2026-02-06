import cv2
import os
import sys

# This ensures Python can find the 'filters' folder inside 'src'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from filters.edges import extract_edges

def process_images(input_dir='input', output_dir='output'):
     # Use absolute paths to avoid confusion
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, '..', 'input')
    output_dir = os.path.join(script_dir, '..', 'output')


    # 1. Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # 2. Define valid extensions
    valid_extensions = ('.jpg', '.jpeg', '.png')

    # 3. Iterate through files in the input folder
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(valid_extensions):
            # Construct full file paths
            input_path = os.path.join(input_dir, filename)
            
            # FIXED: Added 'processed_' prefix to the output filename
            output_filename = f"processed_{filename}"
            output_path = os.path.join(output_dir, output_filename)

            # 4. Load the image
            img = cv2.imread(input_path)

            if img is not None:
                processed_img = extract_edges(img)
                
                # 5. Save the image to the output folder
                cv2.imwrite(output_path, processed_img)
                print(f"Processed: {filename} -> {output_filename}")
            else:
                print(f"Warning: Could not read {filename}. Skipping.")

if __name__ == "__main__":
    process_images()