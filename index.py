import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as pit


capture = cv2.VideoCapture("CW Signal.mp4")

# Tweak and test these
lower = 200   # Lower threshold value
upper = 300  # Upper threshold value

while True:
        ret, frame = capture.read()

        crop = frame[150:1000, 700:1600]

        edge = cv2.Canny(crop, lower, upper)

        cv2.imshow('Edge', edge)

        key = cv2.waitKey(30)
        if key == 27:
                break
        
capture.release()
cv2.destroyAllWindows()
