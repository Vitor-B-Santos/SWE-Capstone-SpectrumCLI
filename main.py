from argparse import ArgumentParser, Namespace
import os
import argparse


    
    
    
def main():
    
    file_name = input('Enter the path to the file: ')
    index_file = 'src/index.py'

    print(f'filename:  {file_name}')
    
    #Define a function to validate the file type
    def is_valid_mp4_file(filename):
    #check if the file is an mp4 file
        if not filename.lower().endswith(".mp4"):
         raise argparse.ArgumentTypeError("Input file must have a '.mp4 extension")
        return filename


    try:
        with open(index_file, 'r') as file:
            code = file.read()
            is_valid_mp4_file(file_name)
            var = {'file_name' : file_name}
            exec(code, var)
    except FileNotFoundError:
        print(f"file not found: {file_name}")
    except Exception as p:
        print(f"An error occurred: {p}")
main()


#Define a function to validate the file type
def is_valid_mp4_file(filename):
    #check if the file is an mp4 file
    if not filename.lower().endswith(".mp4"):
        raise argparse.ArgumentTypeError("Input file must have a '.mp4 extension")
    return filename

#create the main parser argument
parser = ArgumentParser(description="CLI for working analizing Spectrum Analizer mp4 files")

#create subparsers obj for handling commands
subparsers = parser.add_subparsers(dest="command", title="Commands")

# Add an argument for the input MP4 file with the validation function
read_parser = subparsers.add_parser("r", help="Read an MP4 video file")
read_parser.add_argument("input_file", type=is_valid_mp4_file, help="path to the imput mp4 file.")

#Add an argument for the processing of an MP4 file with validation
process_parser = subparsers.add_parser("p", help="Process an MP4 Video file")
process_parser.add_argument("input_file", type=is_valid_mp4_file, help="Path to the input MP4 file")

help_parser = subparsers.add_parser("h", help="Display help information for CLI")
#parse the command-line arguments
args: Namespace = parser.parse_args()

#Preform the action based on the given subcommand
if args.command == "r":
    print(f"Input file '{args.input_file}' is accepted.")

elif args.command == "p":
    print(f"Input file '{args.input_file}' is processing...")
elif args.command == "h":
    parser.print_help()

else:
    #handle case where no subcommand is provided
    print("No subcommand specified. Please try again or use help")

