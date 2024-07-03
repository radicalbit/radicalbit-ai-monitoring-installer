from radicalbit_ai_monitoring.services.fs import FSUtil

from tempfile import TemporaryDirectory

from os import path
import yaml


def test_installed():
    assert FSUtil.installed("test") is False
    with TemporaryDirectory() as dir:
        assert FSUtil.installed(dir) is True


def test_remove_project_structure():
    with TemporaryDirectory() as dir:
        assert FSUtil.installed(dir) is True
        FSUtil.remove_project_structure(dir)
        assert FSUtil.installed(dir) is False


def test_create_project_structure():
    with TemporaryDirectory() as dir:
        _path = path.join(dir, "test")
        assert FSUtil.installed(_path) is False
        FSUtil.create_project_structure(_path, "docker-compose-local.yaml")
        assert FSUtil.installed(_path) is True


def test_update_compose_file_version():
    VERSION = "0.0.1"
    with TemporaryDirectory() as dir:
        _path = path.join(dir, "test")
        FSUtil.create_project_structure(_path, "docker-compose-local.yaml")
        FSUtil.update_compose_file_version(_path, version=VERSION)

        with open(path.join(_path, "docker-compose.yaml")) as f:
            compose_config = yaml.safe_load(f)

        assert (
            compose_config["services"]["ui"]["image"]
            == f"radicalbit/radicalbit-ai-monitoring-ui:{VERSION}"
        )
        assert (
            compose_config["services"]["api"]["image"]
            == f"radicalbit/radicalbit-ai-monitoring-api:{VERSION}"
        )
        assert (
            compose_config["services"]["migrations"]["image"]
            == f"radicalbit/radicalbit-ai-monitoring-migrations:{VERSION}"
        )
