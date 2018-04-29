import cv2
import numpy as np
from track_sim import Camera,Controller
import time

#setup virtual camera frame
cam = Camera((200,200),(320,240))
#include PID controller
PID=Controller(.5,1,time=True)

#setup cv video stream from webcam
capture = cv2.VideoCapture(0)

#setup height and width
capture.set(3,640)
capture.set(4,480)

capture.set(15, -8.0)

#video capture loop
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

    thresh = 40
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
        try:point=keypoints[0].pt
        except: point=(0,0)
        pic=cam.take_image(point)
        print("pic")
        print(pic)
        if pic is not False:
            cam.update_rel(PID.compute(pic))
        else:
            PID.reset()
    except:
        raise
    cam.render(frame)

    #draw the detected blobs over the frames
    frame = cv2.drawKeypoints(frame, keypoints, np.array([]), (255,0,255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    gray = cv2.drawKeypoints(gray, keypoints, np.array([]), (255,0,255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow('detected circles', frame)
    cv2.imshow('grayscale', gray)

    # If its not working, try and adjust thresh
    # Replacing frame with gray to see the thresholded image will make this easier

    #you can adjust this parameter to manually set stream framerate
    cv2.waitKey(int(1000/1000))
