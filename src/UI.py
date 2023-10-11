import click


@click.command()
def greet():
    """This command greets the user."""
    click.echo(
        "Welcome to The Spectrum Analysis Tool! Use the command python UI.py addVid video_path_goes_here to add video for processing"
    )


@click.command()
def farewell():
    """This command bids farewell to the user."""
    click.echo("Goodbye, User!")


@click.group()
def cli():
    """My CLI Tool"""
    pass


# Attach the commands to the group
cli.add_command(greet)
cli.add_command(farewell)

if __name__ == "__main__":
    cli()
