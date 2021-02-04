import picamera
from picamera import PiCamera
import picamera.array
from picamera.array import PiRGBArray
import time
import cv2
import numpy as np
import argparse
import random as rng

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

#dim for image proc. ideally 700x700:
width=640
height=480

#NOFK CLUE what it does (Needed for drawning colors):
rng.seed(12345)

#trackbar callback fucntion does nothing but required for trackbar
def nothing(x):
    pass
 
#create a seperate window named 'controls' for trackbar
cv2.namedWindow('filter')

#create trackbar in 'controls'
cv2.createTrackbar('thresh','filter',0,255,nothing)
cv2.createTrackbar('blur','filter',2,16,nothing)

# allow the camera to warm up
time.sleep(0.1)

#flags for saving images:
detect_image = False
saved_image = False
#counter for the saved image in the path
count  = 0

for frame in camera.capture_continuous(rawCapture, format="bgr",
                                       use_video_port=True):

    # grab the raw NumPy array representing the image, then 
    image = frame.array
    
    #TEST SINGLE IMAGE FROM PATH:
    #img = cv2.imread('/home/pi/Desktop/images/test_images/1.JPG')
    
    #Change variable
    img = image
    
    #resize image
    img=cv2.resize(img,(width,height)) 
    
    #get value for the filters:
    value_th = int(cv2.getTrackbarPos('thresh','filter'))
    value_blur = int(cv2.getTrackbarPos('blur','filter'))
    
    #convert image into gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    
    #Blur image
    blur = cv2.blur(gray,(value_blur,value_blur))
    
    #Apply threshold >> _, >> OPERATOR needed for OpenCV > 4.0.0
    _, threshold = cv2.threshold(blur, value_th, 255, cv2.THRESH_BINARY)
    
    #Find my contours >> ,_ >> OPERATOR needed for OpenCV > 4.0.0
    contours ,_ =cv2.findContours(threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    #Empty vectors ready to fillup with contours:
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    centers = [None]*len(contours)
    radius = [None]*len(contours)
    area = [None]*len(contours)
    
    #Vars for average area calc:
    sum = 0
    average = 0
    
    #loop to get contours 
    for i, c in enumerate(contours):
        contours_poly[i] = cv2.approxPolyDP(c, 3, True)
        boundRect[i] = cv2.boundingRect(contours_poly[i])
        area[i] = cv2.contourArea(contours_poly[i])
        sum = sum + area[i]
    
    average = sum / len(contours)
    
    #Prints the average area of the detected rectangles:
    print(average)
    
    #for Image SAVING
    #Range [min;max] for the detected area:
    if average > 100 and average < 300000:
        detect_image = True
        
        if detect_image is True and saved_image is False:
            count = count + 1
            #SAVE IMAGE >> UNCOMMENT TO SAVE IN THE PATH:
            #cv2.imwrite('/home/pi/Desktop/scipts/images/image'+str(count)+'.jpg',img)
            saved_image = True
        
        #numpy array for the contours drawning:
        drawing = np.zeros((threshold.shape[0], threshold.shape[1], 3), dtype=np.uint8)
        
        #loop for drawning
        for i in range(len(contours)):
            color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
            cv2.drawContours(drawing, contours_poly, i, color)
            cv2.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
              (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
        
        # show detected and processed frame
        cv2.imshow("shapes", drawing)
    
    elif average < 100 or average > 300000:
        detect_image = False
        saved_image = False

    #show applied filters
    cv2.imshow('filter', threshold) 
  
    #show the unprocessed frame
    cv2.imshow("Stream", image)
    
    #Internal Pi function for camera stream. inside for loop. NOFK CLUE what it does (BUT IT WORKS).  
    rawCapture.truncate(0)
    
    #grab key info
    key = cv2.waitKey(1) & 0xFF
    
    #PRESS "Q" key to Exit the program;
    if key == 27 or key == 113:
        break
    
cv2.destroyAllWindows()