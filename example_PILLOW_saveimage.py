from ximea import xiapi
import PIL.Image
from PIL import ExifTags
import os

#create instance for first connected camera 
cam = xiapi.Camera()

#start communication
print('Opening camera...')
cam.open_device()
dType = cam.get_device_info_string('device_type')
dName = cam.get_device_info_string('device_name')

print('Device type:' + str(dType))
print('Device name:' + str(dName))

cam.set_imgdataformat('XI_RGB24')
cam.enable_auto_wb()

#initialize list for exposure time of set
exposure_list = []

#create instance of Image to store image data and metadata
#img = xiapi.Image()

#flips image along y axis
#print('Enabling horizontal flip...')
cam.enable_horizontal_flip()
print(cam.is_horizontal_flip())

#flips image along x axis
#print('Enabling vertical flip...')
cam.enable_vertical_flip()
print(cam.is_vertical_flip())

#path where to save image
save_path = "C:/Users/Martin/Desktop/Ximea_test_Python/Pictures"

for i in range(0, 10):

    #create instance of Image to store image data and metadata
    img = xiapi.Image()

    #settings
    exposureG = ((2**i)*200)
    print(exposureG)
    cam.set_exposure(exposureG)

    #get params for each photo
    real_exposure = cam.get_exposure()
    
    exposure_list.append(real_exposure)

    exposure_burst_count = cam.get_exposure_burst_count()
    #gain = cam.get_gain()
    #gain_selector = cam.get_gain_selector()
    #exposure_time_selector = cam.get_exposure_time_selector()
    #downsampling = cam.get_downsampling()
    #test_pattern_generator_selector = cam.get_test_pattern_generator_selector()
    #test_pattern = cam.get_test_pattern()
    #imgdataformat = cam.get_imgdataformat()
    #image_data_sign = cam.get_image_data_sign()
    #shutter_type = cam.get_shutter_type()
    #sensor_taps = cam.get_sensor_taps()
    #manual_wb = cam.get_manual_wb()
    #wb_kr = cam.get_wb_kr()
    #wb_kr = cam.get_wb_kg()
    #wb_kr = cam.get_wb_kb()
    #width = cam.get_width()
    #height = cam.get_height()
    #interline_exposure_mode = cam.get_interline_exposure_mode()
    #binning_selector = cam.get_binning_selector()
    #decimation_vertical = cam.get_decimation_vertical()
    #limit_bandwidth = cam.get_limit_bandwidth()
    #sensor_bit_depth = cam.get_sensor_bit_depth()
    #output_bit_depth = cam.get_output_bit_depth()
    #image_data_bit_depth = cam.get_image_data_bit_depth()
    #temp = cam.get_temp()
    #device_temperature_ctrl_mode = cam.get_device_temperature_ctrl_mode()
    #gammaY = cam.get_gammaY()
    #gammaC = cam.get_gammaC()
    
    ##!!!!!does not support these params
    #tof_readout_mode = cam.get_tof_readout_mode()
    #lens_aperture_value = cam.get_lens_aperture_value()

    #print('Aperture' , int(lens_aperture_value))
    print('Real exposure of image ' + str(i), int(real_exposure))

    #start data acquisition
    print('Starting data acquisition...')
    cam.start_acquisition()

    #get timestamp on strat of exposure
    timestamp = cam.get_timestamp()
    print('Time of acquisition ', int(timestamp), '[ns]')

    #get data and pass them from camera to img
    cam.get_image(img)

    #get raw data from camera
    data_raw = img.get_image_data_raw()

    #data_raw_list = list(data_raw)

    #get bit by bit data
    #data_matrix = img.get_bytes_per_pixel()

    #create numpy array with data from camera. Dimensions of array are determined
    #by imgdataformat
    #NOTE: PIL takes RGB bytes in opposite order, so invert_rgb_order is True
    data = img.get_image_data_numpy(invert_rgb_order=True)

    img = PIL.Image.fromarray(data, 'RGB') 
    #img.save(f'{save_path}/xi_example_bmp.bmp')
    #img.save(f'{save_path}/xi_example_jpg.jpg')
    #img.save(f'{save_path}/xi_example_png.png')
    img.save(f'{save_path}/xi_vlakno{i}.TIFF')

    #stop data acquisition
    print('Stopping acquisition... \n _________________________________________' )
    cam.stop_acquisition()

#stop communication
cam.close_device() 

with open(os.path.join(save_path, 'priklad den.txt'), 'w') as fp:
    # Convert each float value to a string and join them
    exposure_strings = [str(value) for value in exposure_list]
    fp.write('\n'.join(exposure_strings))  

print('List of exposures', (exposure_list))

## Open the file in write mode
#with open("raw_data.txt", 'w') as file:
#    # Iterate over the list and write each integer followed by a space
#    for data in data_raw:
#        file.write(str(data) + ' ')


print('Done.')
