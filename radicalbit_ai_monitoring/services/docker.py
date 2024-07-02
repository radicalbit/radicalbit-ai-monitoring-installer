import subprocess
from tempfile import TemporaryFile
from typing import List

from radicalbit_ai_monitoring.models.compose_service import ComposeService
from radicalbit_ai_monitoring.models.docker_status import DockerStatus
import json
from os import path
from time import sleep
import sys

import click

from yaspin import yaspin


class DockerUtil:
    def __init__(self, dir: str) -> None:
        self.dir = dir

    @staticmethod
    def dependencies_check() -> None:
        match DockerUtil.check_docker_installation():
            case DockerStatus.DOCKER_NOT_INSTALLED:
                click.echo("Docker can't be found")
                sys.exit(1)
            case DockerStatus.DOWN:
                click.echo("Docker daemon is not running")
                sys.exit(1)

        match DockerUtil.check_docker_compose_installation():
            case DockerStatus.DOCKER_COMPOSE_NOT_INSTALLED:
                click.echo("Docker Compose can't be found")
                sys.exit(1)

    @staticmethod
    def check_docker_installation() -> DockerStatus:
        try:
            ret = subprocess.run(
                ["docker", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except OSError as e:
            from errno import ENOENT

            if e.errno == ENOENT:
                return DockerStatus.DOCKER_NOT_INSTALLED
        if ret.stderr.startswith(b"Cannot connect to the Docker daemon"):
            return DockerStatus.DOWN
        return DockerStatus.UP

    @staticmethod
    def check_docker_compose_installation() -> DockerStatus:
        try:
            subprocess.run(
                ["docker", "compose", "version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except OSError as e:
            from errno import ENOENT

            if e.errno == ENOENT:
                return DockerStatus.DOCKER_COMPOSE_NOT_INSTALLED
        return DockerStatus.UP

    def run_docker_compose_up(self) -> None:
        subprocess.Popen(
            ["docker", "compose", "up", "-d"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=path.abspath(self.dir),
        )
        self.wait_for_containers_ready()

    def run_docker_compose_down(self, *args, verbose: bool = False) -> None:
        with yaspin(text="Stopping the app", color="blue") as spinner:
            p = subprocess.Popen(
                ["docker", "compose", "down", *args],
                cwd=path.abspath(self.dir),
                stdout=None if verbose else subprocess.DEVNULL,
                stderr=None if verbose else subprocess.DEVNULL,
            )
            p.wait()

            if p.returncode != 0:
                spinner.fail("💥")
                click.echo(
                    f"\nError while stopping containers:\n{p.stderr.read().decode()}"
                )
                sys.exit(1)

            spinner.ok("✔")

    def clean_environment(self, verbose: bool = False) -> None:
        self.run_docker_compose_down("-v", "--remove-orphans", verbose=verbose)

    def need_pull(self, services: List[ComposeService]) -> bool:
        p = subprocess.Popen(
            ["docker", "image", "ls", "--format", "{{.Repository}}:{{.Tag}}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=path.abspath(self.dir),
        )
        p.wait()

        if p.returncode != 0:
            click.echo(f"\nError while checking images:\n{p.stderr.read().decode()}")
            sys.exit(1)

        res = p.stdout.read().decode().split("\n")
        return any(f"{s.image}:{s.tag}" not in res for s in services)

    def run_docker_compose_pull(self) -> None:
        with TemporaryFile() as f, yaspin(
            text="Pulling images. This can take a while", color="blue"
        ) as spinner:
            pull_status_proc = subprocess.Popen(
                ["docker", "compose", "pull"],
                stdout=f,
                stderr=f,
                cwd=path.abspath(self.dir),
            )
            while pull_status_proc.poll() is None:
                sleep(0.5)

            if pull_status_proc.returncode != 0:
                spinner.fail("💥")
                click.echo("\nError while pulling images")
                sys.exit(1)

            spinner.ok("✔")

    def wait_for_containers_ready(self) -> None:
        with yaspin(text="Wait for application startup", color="blue") as spinner:
            ps_cmd = ["docker", "compose", "ps", "--all", "--format", "json"]
            while True:
                docker_ps_result = subprocess.run(
                    ps_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=path.abspath(self.dir),
                )
                out = docker_ps_result.stdout.decode("utf-8").split("\n")
                out = filter(lambda x: x != "", out)
                json_res = [json.loads(svc) for svc in out]
                if len(json_res) > 0 and all(
                    [
                        svc["State"] == "running" or svc["State"] == "exited"
                        for svc in json_res
                    ]
                ):
                    break
            spinner.ok("✔")

    def run_app(self, pull: bool = True) -> None:
        if pull:
            self.run_docker_compose_pull()
        self.run_docker_compose_up()
