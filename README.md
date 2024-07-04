# Radicalbit AI Monitoring Installer

This tool is meant to manage the installation of the Radicalbit AI Monitoring Platform [see Open Source repo](https://github.com/radicalbit/radicalbit-ai-monitoring).

## Install

To install you can use [Poetry](https://python-poetry.org/) package manager or via `pip`.

### Using poetry

1. Clone the repository using `git clone https://github.com/radicalbit/radicalbit-ai-monitoring-installer.git`.
1. Move inside the repository using `cd radicalbit-ai-monitoring-installer`.
1. Install poetry using `poetry install`.

### Using pip

Just run `pip install radicalbit-ai-monitoring`.

## Prerequisites

- Python 3.10+
- Docker
- Docker compose

## Usage

If you use poetry to install the project, be sure to activate the shell environment with `poetry shell`.

You can use `rbit-ai-monitoring <command> --help` to get info about the command.

### Commands

- `rbit-ai-monitoring platform install`: install the radicalbit AI Monitoring Platform on the local machine.
- `rbit-ai-monitoring platform uninstall`: uninstall the radicalbit AI Monitoring Platform from the local machine.
- `rbit-ai-monitoring platform down`: stop the execution of the application.
- `rbit-ai-monitoring platform up`: start the execution of the application.
- `rbit-ai-monitoring info`: show info about Radicalbit AI.