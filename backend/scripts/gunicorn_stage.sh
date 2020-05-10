#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py migrate --settings=config.settings.staging
python manage.py collectstatic --noinput --verbosity 0 --settings=config.settings.staging
gunicorn config.wsgi -w 4 --worker-class gevent -b 0.0.0.0:8080 --chdir=/backend --env DJANGO_SETTINGS_MODULE=config.settings.staging
