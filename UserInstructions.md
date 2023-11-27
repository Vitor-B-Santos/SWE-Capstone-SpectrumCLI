# SWE-Capstone

Robbins AFB project 1: Spectrum Analyzer Analysis Tool

## Project Description

Military Flight Test Ranges have a selection of Radio Frequency (RF) Threat Systems, both real and simulated, used for testing Aircraft Electronic Warfare (EW) Systems during flight. The Flight Test Ranges have a radar tracking station that is used to record RF transmissions of the various Threat Systems, both during test and for calibration purposes. The RF transmissions are recorded via video from a Spectrum Analyzer and are provided to the system engineers for the System Under Test (SUT) on DVD. Analysis of this data requires a system engineer to actively watch a selection of video data to verify frequency and amplitude of a specific Threat System. The 402 SWEG at Robins AFB is looking to decrease human interaction by having the information in the video data be analyzed programmatically and transcribed to a numeric format that can be digitally manipulated. The application is able to:

- Recognize and process amplitude on the vertical axis and frequency on the horizontal axis from a video of a Spectrum Analyzer
- Recognize and process the center frequency of a signal and the amplitude of that signal peak (tracking the minimum and maximum amplitudes, as well as providing an average amplitude) from a video of a Spectrum Analyzer
- Store the processed frequency (center) and amplitude (minimum, maximum, and average) information in a CSV formatted file for each detected signal at the signal peak

# User Manual

## Installation

This tool requires an installation of Python 3. To install the latest version of python, you can download it for free from the link:

> https://www.python.org/downloads/

Once Python is installed, ensure that the necessary libraries are installed:

```
pip install opencv-python pandas numpy
```

## Usage

To begin running the Spectrum Analyzer Analysis Tool, execute `SpectrumCLI.py` with the following command:

```
python SpectrumCLI.py
```

A prompt will appear for entering the name of a file. This file must be a video file of a spectrum analyzer ending in the `.mp4` extension.

```
Enter the name of the file in the src/videos folder: <file_name>
```

Next, the program will provide prompts for entering values related to the properties of the spectrum analyzer in the video. If necessary, refer to the video for these values.

**Note that the values of center and span must both be in GHz.**

```
Enter the center (GHz): <center_value>
Enter the span (GHz, 1000 MHz in 1 GHz): <span_value>
```

After these values have been entered, a prompt will ask for a threshold value. This threshold defines the baseline frequency in the video. It allows for filtering for instances in the video when the signal peak goes above this passed threshold value.

**Note that this threshold value must be in dBm.**

```
Enter the threshold for reporting: <threshold_value>
```

Lastly, a window titled "ROI Selector" will appear. In this window, you may click and drag to select a square region within the video. As best as you can, select **only** the region within the video that corresponds to the graph of the spectrum analyzer. Then, press the Enter key to confirm the selection.

Once the video processing is complete, a new csv file containing the timestamped data will be created in the local directory.
