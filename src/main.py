from argparse import ArgumentParser, Namespace
import os
import argparse
import shutil
import cv2


# Define a function to validate the file type
def is_valid_mp4_file(filename):
    # check if the file is an mp4 file
    if not filename.lower().endswith(".mp4"):
        raise argparse.ArgumentTypeError("Input file must have a '.mp4 extension")
    return filename


# create the main parser argument
parser = ArgumentParser(
    description="CLI for working analizing Spectrum Analizer mp4 files"
)

# create subparsers obj for handling commands
subparsers = parser.add_subparsers(dest="command", title="Commands")

# Add an argument for the input MP4 file with the validation function
read_parser = subparsers.add_parser("r", help="Read an MP4 video file")
read_parser.add_argument(
    "input_file", type=is_valid_mp4_file, help="path to the imput mp4 file."
)

# Add an argument for the processing of an MP4 file with validation
process_parser = subparsers.add_parser("p", help="Process an MP4 Video file")
process_parser.add_argument(
    "input_file", type=is_valid_mp4_file, help="Path to the input MP4 file"
)

help_parser = subparsers.add_parser("h", help="Display help information for CLI")
# parse the command-line arguments
args: Namespace = parser.parse_args()

# Preform the action based on the given subcommand
if args.command == "r":
    print(f"Input file '{args.input_file}' is accepted TREY.")

    videos_dir = os.path.join("src", "videos")
    if not os.path.exists(videos_dir):
        os.makedirs(videos_dir)

    destination = os.path.join(videos_dir, os.path.basename(args.input_file))
    shutil.copy(args.input_file, destination)
    print(f"Video copied to '{destination}'")

elif args.command == "p":
    print(f"Input file '{args.input_file}' is processing...")
    
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

elif args.command == "h":
    parser.print_help()

else:
    # handle case where no subcommand is provided
    print("No subcommand specified. Please try again or use help")
