import os
from ximea import xiapi
from PIL import Image
import numpy as np

# Directory to save images
output_dir = 'imgOutput'
os.makedirs(output_dir, exist_ok=True)

# Initialize and open the camera
cam = xiapi.Camera()
cam.open_device()

# Set parameters for burst mode
cam.set_param('exposure_burst_count', 10)
cam.start_acquisition()

# Define different exposure times for each image in microseconds
exposure_times = [10000, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]

# Capture images with different exposure times
for i, exp_time in enumerate(exposure_times):
    cam.set_param('exposure', exp_time)
    img = xiapi.Image()
    cam.get_image(img)

    # Convert image data to numpy array
    img_data = img.get_image_data_numpy()

    # Convert numpy array to PIL Image
    pil_image = Image.fromarray(img_data)

    # Save image as TIFF
    img_filename = os.path.join(output_dir, f'image_{i+1}.tiff')
    pil_image.save(img_filename)

# Stop acquisition and close the camera
cam.stop_acquisition()
cam.close_device()
