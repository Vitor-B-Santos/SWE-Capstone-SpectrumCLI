import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as pit


capture = cv2.VideoCapture("CW Signal.mp4")

object_detect = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

while True:
        ret, frame = capture.read()

        mask = object_detect.apply(frame)
       
        cv2.imshow('Mask', mask)

        key = cv2.waitKey(30)
        if key == 27:
                break
        
capture.release()
cv2.destroyAllWindows()
