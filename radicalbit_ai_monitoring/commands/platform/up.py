import click

from radicalbit_ai_monitoring.services.docker import DockerUtil
from radicalbit_ai_monitoring.services.fs import FSUtil

from pathlib import Path

import sys


@click.command(help="Install the radicalbit-ai-monitoring")
@click.option(
    "--dir",
    "-d",
    default=f"{Path.home()}/rbit-ai-monitoring",
    help="Path of the installation",
    show_default=True,
)
def up(dir: str):
    """Run the radicalbit-ai-monitoring platform"""
    if not FSUtil.installed(dir):
        click.echo("Radicalbit-ai-monitoring is not installed")
        click.echo("Run 'radicalbit-ai-monitoring install --help' for more info")
        sys.exit(1)

    click.echo("Starting radicalbit-ai-monitoring...")
    docker = DockerUtil(dir)

    versions = FSUtil.get_versions(dir)
    pull = docker.need_pull(versions)
    docker.run_app(pull)

    click.echo("Radicalbit-ai-monitoring started successfully")
    # TODO: make the port configurable and update the docker-compose file
    click.echo("You can access it at http://127.0.0.1:5173")
