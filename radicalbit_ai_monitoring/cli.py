import click

from radicalbit_ai_monitoring.commands.platform.platform import platform
from radicalbit_ai_monitoring.commands.info import info
from radicalbit_ai_monitoring import CLI_VERSION


@click.group()
@click.version_option(version=CLI_VERSION, message="%(prog)s %(version)s")
def cli():
    pass


cli.add_command(platform)
cli.add_command(info)
