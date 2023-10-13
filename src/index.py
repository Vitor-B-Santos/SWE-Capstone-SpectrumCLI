import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as pit


capture = cv2.VideoCapture("./videos/CW Signal.mp4")

# Tweak and test these
lower = 200   # Lower threshold value
upper = 300  # Upper threshold value

while True:
        ret, frame = capture.read()

        # Crop Video
        # The frame is treated as a 2D array of pixels.
        # Using array slicing, we specify row_start:row_end, column_start:column_end.
        # Essentially, the top right corner of the video is the coordinate
        # (row_start, column_start) and the bottom right corner is the
        # coordinate (row_end, column_end).
        crop = frame[150:1000, 700:1600]

        edge = cv2.Canny(crop, lower, upper)

        cv2.imshow('Edge', edge)

        key = cv2.waitKey(30)
        if key == 27:
                break
        
capture.release()
cv2.destroyAllWindows()
