import os
from ximea import xiapi
from PIL import Image

# Directory to save images
output_dir = 'imgOutput'
os.makedirs(output_dir, exist_ok=True)

# Initialize and open the camera
cam = xiapi.Camera()
cam.open_device()

# Set exposure time in microseconds (adjust according to your needs)
exposure_time = 10000  # Example exposure time, 10 ms
cam.set_param('exposure', exposure_time)

# Set trigger delay in microseconds (30 ms)
cam.set_param('trigger_delay', 30000)

# Set burst mode to capture two images in rapid succession
cam.set_param('exposure_burst_count', 2)

# Start acquisition
cam.start_acquisition()

# Capture images in burst mode
for i in range(2):
    img = xiapi.Image()
    cam.get_image(img, timeout=5000)  # Set a timeout of 5000 ms (5 seconds)

    # Convert image data to numpy array
    img_data = img.get_image_data_numpy()

    # Convert numpy array to PIL Image
    pil_image = Image.fromarray(img_data)

    # Save image as TIFF
    img_filename = os.path.join(output_dir, f'imgBurst_{i+1}.tiff')
    pil_image.save(img_filename)

    # Clear image memory
    img = None

# Stop acquisition and close the camera
cam.stop_acquisition()
cam.close_device()