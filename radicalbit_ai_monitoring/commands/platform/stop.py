import click

from pathlib import Path

from radicalbit_ai_monitoring.services.docker import DockerUtil
from radicalbit_ai_monitoring.services.fs import FSUtil
import sys


@click.command(help="Stop radicalbit-ai-monitoring")
@click.option(
    "--clean",
    "-c",
    is_flag=True,
    default=False,
    help="Clear the environment volumes",
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
@click.option(
    "--dir",
    "-d",
    default=f"{Path.home()}/radicalbit-ai-monitoring",
    help="Path of the installation",
    show_default=True,
)
def down(clean: bool, dir: str, verbose: bool = False):
    """Stop radicalbit-ai-monitoring"""
    if not FSUtil.installed(dir):
        click.echo("Radicalbit-ai-monitoring is not installed")
        click.echo("Run 'radicalbit-ai-monitoring install --help' for more info")
        sys.exit(1)
    docker = DockerUtil(dir)

    click.echo("Stopping radicalbit-ai-monitoring...")

    if clean and click.confirm(
        "Are you sure you want to clear the environment?", abort=False
    ):
        docker.clean_environment(verbose=verbose)
        click.echo("Radicalbit-ai-monitoring environment cleared successfully")
    else:
        docker.run_docker_compose_down(verbose=verbose)

    click.echo("Radicalbit-ai-monitoring stopped successfully")
