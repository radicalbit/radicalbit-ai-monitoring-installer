import click

from radicalbit_ai_monitoring import RADICALBIT_FIGLET
from radicalbit_ai_monitoring.commands.platform.install import install
from radicalbit_ai_monitoring.commands.platform.stop import down
from radicalbit_ai_monitoring.commands.platform.uninstall import uninstall
from radicalbit_ai_monitoring.commands.platform.up import up

import pyfiglet


@click.group()
def platform():
    """Radicalbit AI Monitoring Platform utilities"""
    message = pyfiglet.figlet_format(RADICALBIT_FIGLET, font="slant")
    click.echo(message)


platform.add_command(install)
platform.add_command(down)
platform.add_command(uninstall)
platform.add_command(up)
