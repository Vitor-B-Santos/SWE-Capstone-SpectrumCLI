import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as pit


capture = cv2.VideoCapture("CW Signal.mp4")

# Tweak and test these
lower = 50   # Lower threshold value
upper = 150  # Upper threshold value

while True:
        ret, frame = capture.read()

        edge = cv2.Canny(frame, lower, upper)

        cv2.imshow('Edge', edge)

        key = cv2.waitKey(30)
        if key == 27:
                break
        
capture.release()
cv2.destroyAllWindows()
