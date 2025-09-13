import os
import glob
import cv2
import numpy as np

def overlay_polygons():
    """
    Overlays blade and vein polygons on leaf images.
    
    This script reads a list of image files from the 'data' directory, finds
    the corresponding '_blade.txt' and '_veins.txt' (or '_vein.txt') polygon files,
    and draws the polygons as filled shapes on the original images. The resulting
    images are saved in a new 'outputs' directory.
    """
    
    # Define relative paths
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
        # Construct the base name (e.g., '300_AHMEUR BOU AHMEUR_ID01')
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        print(f"Processing {base_name}...")
        
        # Load the original image
        img = cv2.imread(img_path)
        if img is None:
            print(f"Error: Could not read image {img_path}")
            continue

        # Create an overlay layer with transparency
        overlay = img.copy()

        # --- Process Blade Polygon ---
        blade_path = os.path.join(data_dir, f'{base_name}_blade.txt')
        if os.path.exists(blade_path):
            blade_coords = np.loadtxt(blade_path, dtype=np.int32)
            # The polygon needs to be reshaped for OpenCV
            blade_coords = blade_coords.reshape((-1, 1, 2))
            
            # Draw the filled polygon on the overlay
            cv2.fillPoly(overlay, [blade_coords], color=(255, 127, 0)) # BGR for dodgerblue
        else:
            print(f"Warning: Blade file not found for {base_name}. Skipping blade overlay.")

        # --- Process Veins Polygon ---
        # Handle both *_veins.txt and *_vein.txt variants
        veins_path = os.path.join(data_dir, f'{base_name}_veins.txt')
        vein_path = os.path.join(data_dir, f'{base_name}_vein.txt')

        if os.path.exists(veins_path):
            veins_coords = np.loadtxt(veins_path, dtype=np.int32)
            veins_coords = veins_coords.reshape((-1, 1, 2))
            cv2.fillPoly(overlay, [veins_coords], color=(255, 0, 255)) # BGR for magenta
        elif os.path.exists(vein_path):
            vein_coords = np.loadtxt(vein_path, dtype=np.int32)
            vein_coords = vein_coords.reshape((-1, 1, 2))
            cv2.fillPoly(overlay, [vein_coords], color=(255, 0, 255)) # BGR for magenta
        else:
            print(f"Warning: Veins/vein file not found for {base_name}. Skipping veins overlay.")

        # --- Combine the layers with desired alpha values ---
        alpha_blade = 0.5
        alpha_veins = 0.8
        
        # Merge the overlay with the original image
        # This is a bit tricky with different alphas for different polygons
        # A better approach is to draw on an empty black image and then use it as a mask
        
        # Start over with a blank canvas for a cleaner approach
        blank_canvas = np.zeros_like(img, dtype=np.uint8)
        
        if os.path.exists(blade_path):
            cv2.fillPoly(blank_canvas, [blade_coords], color=(255, 127, 0)) # BGR for dodgerblue
        
        if os.path.exists(veins_path) or os.path.exists(vein_path):
            vein_file = veins_path if os.path.exists(veins_path) else vein_path
            veins_coords = np.loadtxt(vein_file, dtype=np.int32)
            veins_coords = veins_coords.reshape((-1, 1, 2))
            cv2.fillPoly(blank_canvas, [veins_coords], color=(255, 0, 255)) # BGR for magenta
        
        # Create a final combined image
        final_img = img.copy()
        
        # Apply the overlays with alpha blending
        # For blade (dodgerblue) at 0.5 alpha
        final_img[np.where(np.all(blank_canvas == [255, 127, 0], axis=2))] = (
            final_img[np.where(np.all(blank_canvas == [255, 127, 0], axis=2))] * (1 - alpha_blade) +
            np.array([255, 127, 0]) * alpha_blade
        ).astype(np.uint8)
        
        # For veins (magenta) at 0.8 alpha
        final_img[np.where(np.all(blank_canvas == [255, 0, 255], axis=2))] = (
            final_img[np.where(np.all(blank_canvas == [255, 0, 255], axis=2))] * (1 - alpha_veins) +
            np.array([255, 0, 255]) * alpha_veins
        ).astype(np.uint8)


        # Save the final image
        output_path = os.path.join(outputs_dir, f'{base_name}.png')
        cv2.imwrite(output_path, final_img)
        print(f"Saved to {output_path}")

if __name__ == '__main__':
    overlay_polygons()