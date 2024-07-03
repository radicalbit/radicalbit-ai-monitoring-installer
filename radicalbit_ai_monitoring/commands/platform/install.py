import click

from radicalbit_ai_monitoring import DEFAULT_VERSION, AVAILABLE_VERSIONS
from radicalbit_ai_monitoring.services.docker import DockerUtil
from radicalbit_ai_monitoring.services.fs import FSUtil

from pathlib import Path


@click.command()
@click.option(
    "--dir",
    "-d",
    default=f"{Path.home()}/radicalbit-ai-monitoring",
    help="The name of the directory to create",
    show_default=True,
)
@click.option(
    "--version",
    "-v",
    default=DEFAULT_VERSION,
    help="The version of the docker image to use",
    show_default=True,
    type=click.Choice(AVAILABLE_VERSIONS),
)
@click.option(
    "--overwrite",
    "-o",
    is_flag=True,
    default=False,
    help="Overwrite the current installation",
    show_default=True,
)
def install(dir: str, version: str, overwrite: bool = False):
    """Install the radicalbit-ai-monitoring"""
    click.echo(f"Installing radicalbit-ai-monitoring {version}")
    # Check if docker is installed and up and running
    docker = DockerUtil(dir)
    docker.dependencies_check()

    if FSUtil.installed(dir) or overwrite:
        if click.confirm(
            f"Found an existing installation in {dir}.\nDo you want to overwrite it?",
            abort=True,
        ):
            docker.clean_environment()
            FSUtil.remove_project_structure(dir)

    FSUtil.create_project_structure(dir, "docker-compose-local.yaml")

    if version != DEFAULT_VERSION:
        FSUtil.update_compose_file_version(dir, version=version)

    # run the compose file
    docker.run_docker_compose_down()
    versions = FSUtil.get_versions(dir)
    pull = docker.need_pull(versions)
    docker.run_app(pull)

    click.echo("\nRadicalbit-ai-monitoring started successfully")
    # TODO: make the port configurable and update the docker-compose file
    click.echo("You can access it at http://127.0.0.1:5173")
