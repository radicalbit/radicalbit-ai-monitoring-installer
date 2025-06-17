import os.path as path
import radicalbit_ai_monitoring


# x-release-please-start-version
CLI_VERSION = "0.11.0"
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
    "init-data": "postgres:15.7-alpine",
    "minio-mirror": "minio/minio:latest",
    "k3s": "rancher/k3s:v1.30.1-k3s1",
    "clickhouse": "clickhouse/clickhouse-server:latest",
    "otel-collector": "otel/opentelemetry-collector-contrib:latest",
}

ALL_IMAGES = {**RBIT_IMAGES, **EXTERNAL_IMAGES}

DEFAULT_VERSION = "latest"

OSS_REPO = "https://github.com/radicalbit/radicalbit-ai-monitoring"
OSS_REPO_API = "https://api.github.com/repos/radicalbit/radicalbit-ai-monitoring"

AVAILABLE_VERSIONS = ["latest", "v1.3.0", "v1.2.0", "v1.1.0", "v1.0.1"]

RADICALBIT_FIGLET = "Radicalbit AI Monitoring"
