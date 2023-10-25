import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as pit


capture = cv2.VideoCapture("./videos/CW Signal.mp4")

# Tweak and test these
lower = 190   # Lower threshold value
upper = 200   # Upper threshold value

while True:
        ret, frame = capture.read()

        # Crop Video
        # The frame is treated as a 2D array of pixels.
        # Using array slicing, we specify row_start:row_end, column_start:column_end.
        # Essentially, the top right corner of the video is the coordinate
        # (row_start, column_start) and the bottom right corner is the
        # coordinate (row_end, column_end).
        crop = frame[150:900, 700:1600]

        # Convert the grayscale image to a binary mask
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        gray = cv2.medianBlur(gray, 5)

        # Detect Edges
        canny = cv2.Canny(gray, lower, upper)

        # Make edge lines thicker
        kernel = np.ones((5, 5), np.uint8)
        binary_mask = cv2.dilate(canny, kernel, iterations=3)

        # Identify shapes in black and white mask
        # Find contours returns a list of contour object which we can work with
        # individually (contours[0], contours[1], etc.). If we can identify which
        # contour is the RF signal in each frame then we should be able to get 
        # data such as its x,y position and its height and width.
        contours, hierarchy = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contour with largest area
        # (Doesn't seem to do anything, can't figure out why)
        # c = max(contours, key=cv2.contourArea)
        # cv2.drawContours(binary_mask, [c], 0, (0, 255, 0), 3)

        cv2.imshow('Edge', binary_mask)

        key = cv2.waitKey(30)
        if key == 27:
                break
        
capture.release()
cv2.destroyAllWindows()
