#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

python manage.py makemigrations --settings=config.settings.development
python manage.py migrate --settings=config.settings.development
python manage.py collectstatic --noinput --settings=config.settings.development --verbosity 0
python manage.py runserver_plus 0.0.0.0:8000 --settings=config.settings.development
