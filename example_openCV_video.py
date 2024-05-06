from ximea import xiapi
import cv2
import time

#create instance for first connected camera 
cam = xiapi.Camera()

#start communication
print('Opening first camera...')
cam.open_device()

#settings
cam.set_exposure(200000)
cam.enable_auto_wb()
cam.set_imgdataformat('XI_RGB24')

#flips image along y axis
#print('Enabling horizontal flip...')
cam.enable_horizontal_flip()
print(cam.is_horizontal_flip())

#flips image along x axis
#print('Enabling vertical flip...')
cam.enable_vertical_flip()
print(cam.is_vertical_flip())

#create instance of Image to store image data and metadata
img = xiapi.Image()

#start data acquisition
print('Starting data acquisition...')
cam.start_acquisition()

try:
    print('Starting video. Press CTRL+C to exit.')
    t0 = time.time()
    while True:
        
        #get data and pass them from camera to img
        cam.get_image(img)

        #create numpy array with data from camera. Dimensions of the array are 
        #determined by imgdataformat
        data = img.get_image_data_numpy()

        #show acquired image with time since the beginning of acquisition
        font = cv2.QT_FONT_NORMAL
        text = '{:5.2f}'.format(time.time()-t0)
        cv2.putText(
            data, text, (900,150), font, 4, (255, 255, 255), 2
            )
        #cv2.imshow('XiCAM example', data)

        scaling_factor = min(1200.0 / data.shape[1], 800.0 / data.shape[0])

        # Resize the image for display
        resized_image = cv2.resize(data, None, fx=scaling_factor, fy=scaling_factor)

        # Create a window with the specified name
        cv2.namedWindow('video', cv2.WINDOW_NORMAL)

        # Show the resized image in the window
        cv2.imshow('video', resized_image)

        cv2.waitKey(1)
        
except KeyboardInterrupt:
    cv2.destroyAllWindows()

#stop data acquisition
print('Stopping acquisition...')
cam.stop_acquisition()

#stop communication
cam.close_device()

print('Done.')
