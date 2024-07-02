from radicalbit_ai_monitoring import MODULE_PATH
from radicalbit_ai_monitoring import DEFAULT_VERSION, ALL_IMAGES, RBIT_IMAGES
from radicalbit_ai_monitoring.models.compose_service import ComposeService

from os import path, makedirs
from shutil import copy2, copytree, rmtree
import yaml

from typing import List


class FSUtil:
    @staticmethod
    def create_project_structure(dir: str, compose_file: str) -> None:
        resources_path = path.abspath(path.join(MODULE_PATH, "resources"))
        docker_resources_path = path.abspath(path.join(resources_path, "docker"))
        compose_path = path.abspath(path.join(resources_path, compose_file))

        makedirs(dir)
        # copy in the current directory
        copy2(compose_path, path.join(dir, "docker-compose.yaml"))
        copytree(docker_resources_path, path.join(dir, "docker"))

    @staticmethod
    def remove_project_structure(dir: str) -> None:
        rmtree(dir, ignore_errors=False)

    @staticmethod
    def installed(dir: str) -> bool:
        return path.exists(dir)

    @staticmethod
    def get_versions(dir: str) -> List[ComposeService]:
        compose_path = path.abspath(path.join(dir, "docker-compose.yaml"))
        with open(compose_path) as f:
            compose_config = yaml.safe_load(f)
        return [
            ComposeService(
                name=service,
                image=compose_config["services"][service]["image"].split(":")[0],
                tag=compose_config["services"][service]["image"].split(":")[1],
            )
            for service in ALL_IMAGES.keys()
        ]

    @staticmethod
    def update_compose_file_version(
        dir: str,
        compose_file: str = "docker-compose.yaml",
        version: str = DEFAULT_VERSION,
    ) -> None:
        compose_path = path.abspath(path.join(dir, compose_file))
        with open(compose_path) as f:
            compose_config = yaml.safe_load(f)

        # update version
        for service, image in RBIT_IMAGES.items():
            compose_config["services"][service]["image"] = f"{image}:{version}"

        with open(compose_path, "w") as f:
            yaml.dump(compose_config, f)
