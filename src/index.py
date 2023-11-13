import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as pit
import datetime
import csv_utils

capture = cv2.VideoCapture("./videos/Pulsed Signal.mp4")

# Properties of spectrum analyzer
scale = -100
center = 1.0 # GHz
span = 0.1 # GHz

# Canny detect threshold values
lower = 180
upper = 200

amplitudes = []
frequencies = []
frame_data = []

_, first_frame = capture.read()

instructions = [
    "Instructions:",
    "- Click and drag to select ROI",
    "- Press 'Enter' to confirm selection",
    "- Cancel the selection process by pressing c button!",
    "- Press 'q' to exit"
]

for i, instruction in enumerate(instructions):
    cv2.putText(first_frame, instruction, (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

roi = cv2.selectROI(first_frame)
cv2.destroyWindow("ROI Selection Instructions")

while True:
    ret, frame = capture.read()

    if frame is None:
        break

    # Crop video based on ROI
    crop = frame[int(roi[1]):int(roi[1]+roi[3]),
                 int(roi[0]):int(roi[0]+roi[2])]
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
    contours, _ = cv2.findContours(
        binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Find contour with largest area
    c = max(contours, key=cv2.contourArea)

    # Skip frames when the largest contour does not meet a minimum size
    # This is to avoid recording data in the frames where the radio signal briefly disappears
    if int(cv2.contourArea(c)) > 30_000:
        binary_mask = cv2.drawContours(
            crop, [c], -1, (0, 255, 0), 3, lineType=cv2.LINE_AA
        )

        # The coordinate (x,y) is the top left corner of the rectangle. w and h are the
        # amount of offset from x and y respectively, aka width and height.
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(crop, (x, y), (x + w, y + h), (255, 0, 0), 2)

        non_zero = np.nonzero(binary_mask)
        frequency = (non_zero[0][0] / img_width) * (span * 10) + (center / 2)
        frequencies.append(frequency)
		
        # Use y position to calculate amplitude
        amp = (y / img_height) * scale
        amplitudes.append(amp)

    cv2.imshow("Edge", crop)
    key = cv2.waitKey(30)
    if key == 27:
        break

    # get the current timestampt
    timestamp = datetime.datetime.now()

capture.release()
cv2.destroyAllWindows()

# data processing
if amplitudes:
    max_amp = max(amplitudes)
    min_amp = min(amplitudes)
    average_amp = sum(amplitudes) / len(amplitudes)

    # Frequency calculation
    average_freq = sum(frequencies) / len(frequencies)
    print(average_freq)
    # add data from current frame to list
    # frame_data.append([timestamp, min_amp, max_amp, average_amp, frequency])

df = pd.DataFrame(
    frame_data,
    columns=[
        "Timestamp",
        "Min Amplitude",
        "Max Amplitude",
        "Average Amplitude",
        "Frequency",
    ],
)

csv_utils.save_as_csv(df)

print(df)
print("done")
