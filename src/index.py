import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as pit


capture = cv2.VideoCapture("./videos/CW Signal.mp4")

# Properties of spectrum analyzer
scale = -100
center = 1.0 
span = 100.0

# Canny detect threshold values
lower = 190
upper = 200 

amplitudes = []

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
        img_height, img_width = crop.shape[:2]

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
        # individually (contours[0], contours[1], etc.).
        contours, hierarchy = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find contour with largest area
        c = max(contours, key=cv2.contourArea)

        # Skip frames when the largest contour does not meet a minimum size
        # This is to avoid recording data in the frames where the radio signal briefly disappears
        if int(cv2.contourArea(c)) > 30_000:  
                binary_mask = cv2.drawContours(crop, [c], -1, (0, 255, 0), 3, lineType=cv2.LINE_AA)

                # The coordinate (x,y) is the top left corner of the rectangle. w and h are the
                # amount of offset from x and y respectively, aka width and height.
                x,y,w,h = cv2.boundingRect(c)        
                cv2.rectangle(crop, (x,y), (x+w,y+h), (255,0,0), 2) 

                # Use y position to calculate amplitude
                amp = (y / img_height) * scale
                amplitudes.append(amp)
        
        cv2.imshow('Edge', crop)
        key = cv2.waitKey(30)
        if key == 27:
                break
        
capture.release()
cv2.destroyAllWindows()

# Data Processing
max_amp = max(amplitudes)
min_amp = min(amplitudes)
average_amp = sum(amplitudes) / len(amplitudes)

print("Max Amplitude: " + str(max_amp) + " dBm")
print("Min Amplitude: " + str(min_amp) + " dBm")
print("Average Amplitude: " + str(average_amp) + " dBm")