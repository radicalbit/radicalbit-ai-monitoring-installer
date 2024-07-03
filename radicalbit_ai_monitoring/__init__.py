import os.path as path
import radicalbit_ai_monitoring


# x-release-please-start-version
CLI_VERSION = "0.0.1"
# x-release-please-end
MODULE_PATH = path.abspath(path.dirname(radicalbit_ai_monitoring.__file__))

RBIT_IMAGES = {
    "api": "radicalbit/radicalbit-ai-monitoring-api",
    "ui": "radicalbit/radicalbit-ai-monitoring-ui",
    "migrations": "radicalbit/radicalbit-ai-monitoring-migrations",
}

EXTERNAL_IMAGES = {
    "postgres": "postgres:15.7-alpine",
    "minio": "minio/minio:latest",
    "createbuckets": "minio/mc:latest",
    "k3s": "rancher/k3s:v1.30.1-k3s1",
}

ALL_IMAGES = {**RBIT_IMAGES, **EXTERNAL_IMAGES}

DEFAULT_VERSION = "latest"

OSS_REPO = "https://github.com/radicalbit/radicalbit-ai-monitoring"
OSS_REPO_API = "https://api.github.com/repos/radicalbit/radicalbit-ai-monitoring"

AVAILABLE_VERSIONS = ["latest", "v0.8.2"]

RADICALBIT_FIGLET = "Radicalbit AI Monitoring"
