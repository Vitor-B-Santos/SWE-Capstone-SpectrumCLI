import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
from VideoTimestamp import VideoTimestamp

capture = cv2.VideoCapture(file_name)
frame_rate = capture.get(cv2.CAP_PROP_FPS)
video_timestamp = VideoTimestamp(frame_rate)

# Properties of spectrum analyzer
scale = -100
center = float(entered_center)  # GHz
span = float(entered_span)  # GHz
threshold = float(entered_threshold)

amplitudes = []
frequencies = []
frame_data = []

# roi selector
_, first_frame = capture.read()

instructions = [
    "Instructions:",
    "- Click and drag to select the dimensions around the graph only",
    "- Press 'Enter' to confirm selection",
    "- Cancel the selection process by pressing c button!",
    "- Press 'q' to exit",
]

for i, instruction in enumerate(instructions):
    cv2.putText(
        first_frame,
        instruction,
        (10, 30 + i * 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2,
    )

roi = cv2.selectROI(first_frame)
# cv2.destroyWindow("ROI Selection Instructions")

# Canny detect threshold values
mean_intensity = np.mean(cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY))
std_dev_intensity = np.std(cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY))

if std_dev_intensity < 50:
    # lower = int(max(0, mean_intensity - std_dev_intensity))
    # upper = int(min(255, mean_intensity + std_dev_intensity))
    lower = 145
    upper = 210
else:
    lower = 190
    upper = 230


while True:
    ret, frame = capture.read()

    if frame is None:
        break

    video_timestamp.update_frame_count()
    formatted_time = video_timestamp.get_formatted_time()

    # Crop video based on ROI
    crop = frame[int(roi[1]) : int(roi[1] + roi[3]), int(roi[0]) : int(roi[0] + roi[2])]
    img_height, img_width = crop.shape[:2]

    # Convert to grayscale and blur to remove noise
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    mask = cv2.inRange(blurred, lower, upper)

    # Detect Edges
    canny = cv2.Canny(mask, lower, upper)

    # Make edge lines thicker
    kernel = np.ones((5, 5), np.uint8)
    binary_mask = cv2.dilate(canny, kernel, iterations=4)
    binary_mask = cv2.erode(binary_mask, kernel, iterations=1)

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
    if int(cv2.contourArea(c)) > 20_000:
        cv2.drawContours(crop, [c], -1, (0, 255, 0), 3, lineType=cv2.LINE_AA)

        # The coordinate (x,y) is the top left corner of the rectangle. w and h are the
        # amount of offset from x and y respectively, aka width and height.
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(crop, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Determine the (x,y) position of the highest peak that belongs to the contour
        # Useful documentation https://docs.opencv.org/3.4/d1/d32/tutorial_py_contour_properties.html
        highest_point = tuple(c[c[:, :, 1].argmin()][0])

        # Use x position of highest point on contour to calculate frequency
        scaling_factor = span / img_width
        frequency = (center - span / 2) + (highest_point[0] * scaling_factor)
        frequencies.append(frequency)

        # Use y position to calculate amplitude
        amp = (highest_point[1] / img_height) * scale
        amplitudes.append(amp)

        frame_data.append([formatted_time, amp, frequency])

    cv2.imshow("Edge", crop)
    # cv2.imshow("Edge", canny)
    key = cv2.waitKey(30)
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()

# data processing
if amplitudes:
    max_amp = max(amplitudes)
    min_amp = min(amplitudes)
    average_amp = sum(amplitudes) / len(amplitudes)
    print(average_amp)

    # Frequency calculation
    max_freq = max(frequencies)
    average_freq = sum(frequencies) / len(frequencies)
    print(average_freq)

df = pd.DataFrame(
    frame_data,
    columns=[
        "Timestamp",
        "amplitudes",
        "frequencies",
    ],
)


def convert_to_csv(df):
    # Check if the DataFrame is valid
    if df is None or df.empty:
        print("The DataFrame is empty or not defined.")
        return

    # Generate a timestamp-based filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.csv"

    # Check if the output directory exists, if not, create it
    output_dir = "output_csvs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Construct the full file path
    file_path = os.path.join(output_dir, filename)

    # Save the DataFrame as a CSV
    df.to_csv(file_path, index=False)
    print(f"DataFrame saved as CSV in '{file_path}'")


print("Frame data has been collected. Awaiting processing...")

df["Minimum Amplitude"] = min_amp
df["Maximum Amplitude"] = max_amp
df["Average Amplitude"] = average_amp
df["Maximum Frequency"] = max_freq
df["Average Frequency"] = average_freq

# filter dataframe using user defined threshold value
filtered_df = df[df["amplitudes"] > threshold]

# Check if the filtered dataframe is not empty before converting to csv
if not filtered_df.empty:
    # convert updated dataframe into csv
    convert_to_csv(filtered_df)
    print("Frame data has been processed and stored in new .csv file")
else:
    print("No data met the threshold criteria.")
