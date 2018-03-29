import cv2
import numpy as np
from track_sim import Camera,Controller
import time
from servo import ArduServo


servo=ArduServo('/dev/ttyACM0')
servo.open()
servo.write(180)

cam = Camera((400,400),(300,200))
PID=Controller(.01,0.005,.01,time=True)
capture = cv2.VideoCapture(0)
capture.set(3,1000)
capture.set(4,500)
#capture.set(CV_CAP_PROP_FPS,1) #framerate
capture.set(15, -8.0)

colors = {
    "red":(0,0,255),
    "yellow":(0,255,255),
    "green":(0,255,0)
    }

while(1):

    # video feed (image captured in frame)
    ret, frame = capture.read()

    # convert to grayscale for thresholding
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # smoothing filter
    gray = cv2.GaussianBlur(gray, (3,3), 1)

    # Threshold the image to take advantage of contrast between white paper and dark blob
    # Thresh is for tweaking in different lighting (lower thresh = blob needs to be darker to be thresholded)
    # I used 120 in poor lighting, and I only drew a blob in pencil on some looseleaf and it worked fine
    # If you use a marker or something on white printer paper this will work even better

    thresh = 80
    gray[gray < thresh] = 0
    gray[gray > 0] = 255

    # Morphological transformation to remove inconsistent specs within blob threshold
    kernal = np.ones((3, 3), np.uint8)
    cv2.erode(gray, kernal)

    # Blob detection and marking, may have to change depending on what you draw on the paper
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = 0
    params.maxThreshold = 256
    params.filterByArea = True
    params.minArea = 600
    params.filterByCircularity = True
    params.minCircularity = 0.75
    params.filterByConvexity = True
    params.minConvexity = 0.5
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(gray)
    try:
        try:pointD=keypoints[0].pt
        except: pointD=(0,0)
        #print('point')
        #print(pointD)
        #cv2.rectangle(frame,tuple((np.array(pointD)-100).astype(int)),tuple((np.array(pointD)+100).astype(int)),(255,0,0),10)
        #print("good so far..")

        pic=cam.take_image(pointD)
        #print("pic")
        #print(pic)
        if pic is not False:
            comp=PID.compute(pic)
            #cam.update_rel(comp)
            servo.write(servo.pos-int(.2*comp[1]))
        else:
            PID.reset()
    except:
        raise
    cam.render(frame)
    frame = cv2.drawKeypoints(frame, keypoints, np.array([]), (255,0,255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    gray = cv2.drawKeypoints(gray, keypoints, np.array([]), (255,0,255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow('detected circles', frame)
    cv2.imshow('grayscale', gray)

    # If its not working, try and adjust thresh
    # Replacing frame with gray to see the thresholded image will make this easier

    cv2.waitKey(1)
