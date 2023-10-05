import click
import shutil
import subprocess


@click.group()
def cli():
    "Welcome to the Spectrum Analysis Tool!"
    pass


def addVid(video_file_path):
    "Add a video for processing"

    if not video_file_path:
        click.echo("Video file not found.")
        return

    destination_path = "SWE-Capstone/"
    shutil.copy(video_file_path, destination_path)
    click.echo(f"Added video into program")
    pass


def run():
    "Run the program"

    python_path = "SWE-Capstone/index.py"
    result = subprocess.run(["python", python_path], capture_output=True, text=True)
    if result.returncode == 0:
        click.echo("Success!")
    else:
        click.echo("Error executing code")
        click.echo(result.stderr)
    pass
