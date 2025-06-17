import click

from radicalbit_ai_monitoring.services.docker import DockerUtil
from radicalbit_ai_monitoring.services.fs import FSUtil

from pathlib import Path
import sys


@click.command()
@click.option(
    "--dir",
    "-d",
    default=f"{Path.home()}/rbit-ai-monitoring",
    help="Path of the installation",
    show_default=True,
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Enable verbose mode",
    show_default=True,
)
@click.confirmation_option(
    prompt="Are you sure you want to uninstall radicalbit-ai-monitoring?",
    help="Confirm that you want to uninstall",
)
def uninstall(dir: str, verbose: bool = False):
    """Uninstall the radicalbit-ai-monitoring"""
    if not FSUtil.installed(dir):
        click.echo("Radicalbit-ai-monitoring is not installed. Nothing to do")
        sys.exit(1)
    docker = DockerUtil(dir)

    click.echo("Uninstalling radicalbit-ai-monitoring...")

    docker.clean_environment(verbose=verbose)
    FSUtil.remove_project_structure(dir)

    click.echo("Radicalbit-ai-monitoring uninstalled successfully")
