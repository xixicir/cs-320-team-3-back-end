#! /usr/bin/env bash
set -euxo pipefail
docker-compose down --volumes
docker volume rm -f cs-320-team-3-back-end_postgres_data