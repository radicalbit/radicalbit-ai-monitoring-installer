from enum import Enum


class DockerStatus(Enum):
    UP = 0
    DOWN = 1
    DOCKER_NOT_INSTALLED = 2
    DOCKER_COMPOSE_NOT_INSTALLED = 3
