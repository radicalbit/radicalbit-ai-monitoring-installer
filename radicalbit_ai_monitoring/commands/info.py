import click
import pyfiglet

from radicalbit_ai_monitoring import CLI_VERSION, OSS_REPO, RADICALBIT_FIGLET


@click.command()
def info():
    """Show Info About Radicalbit AI"""
    message = pyfiglet.figlet_format(RADICALBIT_FIGLET, font="slant")
    click.echo(message)
    click.echo(f"CLI Version: {CLI_VERSION}")
    click.echo("Author: https://github.com/radicalbit")
    click.echo(f"Radicalbit AI Monitoring GitHub: {OSS_REPO}")
