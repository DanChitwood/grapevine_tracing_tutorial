import os
import glob
import cv2
import numpy as np

def overlay_polygons():
    """
    Overlays blade and vein polygons on leaf images and saves them as JPEGs.
    
    This script reads a list of image files from the 'data' directory, finds
    the corresponding '_blade.txt' and '_veins.txt' (or '_vein.txt') polygon files,
    and draws the polygons as filled shapes on the original images. The resulting
    images are saved as JPEG files in a new 'outputs' directory with a quality setting
    of 95 to balance file size and visual quality.
    """
    
    # Define relative paths
    # These paths are relative to the script's location in the 'scripts' directory
    data_dir = os.path.join('..', 'data')
    outputs_dir = os.path.join('..', 'outputs')

    # Create outputs directory if it doesn't exist
    os.makedirs(outputs_dir, exist_ok=True)

    # Get a list of all image files, case-insensitively
    image_extensions = ['jpg', 'jpeg', 'png', 'tif', 'tiff']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(data_dir, f'*.{ext}'), recursive=False))
        image_files.extend(glob.glob(os.path.join(data_dir, f'*.{ext.upper()}'), recursive=False))
    
    if not image_files:
        print("No image files found in the data directory.")
        return

    for img_path in image_files:
        # Construct the base name of the file (e.g., '300_AHMEUR BOU AHMEUR_ID01')
        # This is used to find the corresponding .txt files
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        print(f"Processing {base_name}...")
        
        # Load the original image
        img = cv2.imread(img_path)
        if img is None:
            print(f"Error: Could not read image {img_path}")
            continue

        # Create a blank canvas of the same size as the image for drawing overlays
        blank_canvas = np.zeros_like(img, dtype=np.uint8)
        
        # --- Process Blade Polygon ---
        blade_path = os.path.join(data_dir, f'{base_name}_blade.txt')
        blade_coords = None
        if os.path.exists(blade_path):
            try:
                blade_coords = np.loadtxt(blade_path, dtype=np.int32)
                # Reshape the coordinates for OpenCV's fillPoly function
                blade_coords = blade_coords.reshape((-1, 1, 2))
                # Draw the filled blade polygon in dodgerblue on the blank canvas
                cv2.fillPoly(blank_canvas, [blade_coords], color=(255, 127, 0)) # BGR for dodgerblue
            except Exception as e:
                print(f"Warning: Could not process blade file {blade_path}. Error: {e}")
        else:
            print(f"Warning: Blade file not found for {base_name}. Skipping blade overlay.")

        # --- Process Veins Polygon ---
        # Check for both '_veins.txt' and '_vein.txt' variants
        veins_path = os.path.join(data_dir, f'{base_name}_veins.txt')
        vein_path_variant = os.path.join(data_dir, f'{base_name}_vein.txt')
        
        veins_coords = None
        if os.path.exists(veins_path):
            try:
                veins_coords = np.loadtxt(veins_path, dtype=np.int32)
                veins_coords = veins_coords.reshape((-1, 1, 2))
                # Draw the filled veins polygon in magenta on the blank canvas
                cv2.fillPoly(blank_canvas, [veins_coords], color=(255, 0, 255)) # BGR for magenta
            except Exception as e:
                print(f"Warning: Could not process veins file {veins_path}. Error: {e}")
        elif os.path.exists(vein_path_variant):
            try:
                veins_coords = np.loadtxt(vein_path_variant, dtype=np.int32)
                veins_coords = veins_coords.reshape((-1, 1, 2))
                # Draw the filled veins polygon in magenta on the blank canvas
                cv2.fillPoly(blank_canvas, [veins_coords], color=(255, 0, 255)) # BGR for magenta
            except Exception as e:
                print(f"Warning: Could not process vein file {vein_path_variant}. Error: {e}")
        else:
            print(f"Warning: Veins/vein file not found for {base_name}. Skipping veins overlay.")

        # --- Combine the original image with the overlayed polygons ---
        final_img = img.copy()
        
        # Define alpha blending values
        alpha_blade = 0.5
        alpha_veins = 0.8
        
        # Apply the blade overlay (dodgerblue)
        # We find pixels on the blank canvas that are dodgerblue
        # and blend them with the corresponding pixels in the original image.
        if blade_coords is not None:
            blade_mask = np.all(blank_canvas == [255, 127, 0], axis=2)
            final_img[blade_mask] = (
                final_img[blade_mask] * (1 - alpha_blade) +
                np.array([255, 127, 0]) * alpha_blade
            ).astype(np.uint8)
        
        # Apply the veins overlay (magenta)
        # We find pixels on the blank canvas that are magenta
        # and blend them with the corresponding pixels in the original image.
        if veins_coords is not None:
            veins_mask = np.all(blank_canvas == [255, 0, 255], axis=2)
            final_img[veins_mask] = (
                final_img[veins_mask] * (1 - alpha_veins) +
                np.array([255, 0, 255]) * alpha_veins
            ).astype(np.uint8)

        # --- Save the final image as a JPEG ---
        # This reduces file size compared to PNG.
        # cv2.IMWRITE_JPEG_QUALITY controls the compression level (0-100).
        # A value of 95 provides a good balance between quality and file size.
        output_filename = f'{base_name}.jpg'
        output_path = os.path.join(outputs_dir, output_filename)
        cv2.imwrite(output_path, final_img, [cv2.IMWRITE_JPEG_QUALITY, 95])
        print(f"Saved output to {output_path}")

if __name__ == '__main__':
    overlay_polygons()