import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as pit


capture = cv2.VideoCapture("./videos/CW Signal.mp4")

# Tweak and test these
lower = 190   # Lower threshold value
upper = 200   # Upper threshold value
contour_areas = []

while True:
        ret, frame = capture.read()
        
        if frame is None:
                break
        # Crop Video
        # The frame is treated as a 2D array of pixels.
        # Using array slicing, we specify row_start:row_end, column_start:column_end.
        # Essentially, the top right corner of the video is the coordinate
        # (row_start, column_start) and the bottom right corner is the
        # coordinate (row_end, column_end).
        crop = frame[200:900, 700:1600]

        # Convert to grayscale and blur to remove noise
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        blur = cv2.medianBlur(gray, 5)

        # Detect Edges
        canny = cv2.Canny(blur, lower, upper)

        # Make edge lines thicker
        kernel = np.ones((5, 5), np.uint8)
        binary_mask = cv2.dilate(canny, kernel, iterations=5)

        # Identify shapes in black and white mask
        # Find contours returns a list of contour object which we can work with
        # individually (contours[0], contours[1], etc.). If we can identify which
        # contour is the RF signal in each frame then we should be able to get 
        # data such as its x,y position and its height and width.
        contours, hierarchy = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contour with largest area
        c = max(contours, key=cv2.contourArea)
        contour_areas.append(cv2.contourArea(c))
        # Skip frames the largest contour does not meet a minimum size
        # This is to avoid recording data in the frames where the radio signal briefly disappears
        if int(cv2.contourArea(c)) > 30_000:  
                binary_mask = cv2.drawContours(crop, [c], -1, (0, 255, 0), 3, lineType=cv2.LINE_AA)
                
                cv2.imshow('Edge', crop)

                key = cv2.waitKey(30)
                if key == 27:
                        break
        
capture.release()
cv2.destroyAllWindows()

average_area = int(sum(contour_areas) / len(contour_areas))
print("Average size of largest contour : " + str(average_area))
