#!/usr/bin/env bash

set -o errexit
set -o pipefail
cmd="$@"

# N.B. If only .env files supported variable expansion...
export CELERY_BROKER_URL="${REDIS_URL}"

if [ -z "${POSTGRES_USER}" ]; then
    base_postgres_image_default_user='postgres'
    export POSTGRES_USER="${base_postgres_image_default_user}"
fi
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

function postgres_ready(){
python << END
import sys
import psycopg2
import environ

try:
    env = environ.Env()
    dbname = env.str('POSTGRES_DB')
    user = env.str('POSTGRES_USER')
    password = env.str('POSTGRES_PASSWORD')
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host='postgres', port=5432)
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing..."
exec $cmd
