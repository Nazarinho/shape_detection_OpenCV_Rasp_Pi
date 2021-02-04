# shape_detection_OpenCV_Rasp_Pi
Needs to be run on Raspberry Pi with opencv higher than 4.0.0 and python 3.7. 

Initially opens 2 windows: 

>>Window for the Filter with trackbar (blur and threshold params). 

>>Window with the actual unprocessed stream.

If the condition of the detected area of the rectangle is met, the 3rd window is opened:

>>Window with the detected shape drawn in the frame.

There is a possibility to save the original image with the desired shape detected in a local directory.

UNCOMMENT line 106
