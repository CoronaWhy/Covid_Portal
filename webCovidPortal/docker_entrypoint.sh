#! /bin/bash
set -e


python3 manage.py migrate contenttypes
python3 manage.py migrate auth
python3 manage.py migrate admin
python3 manage.py migrate

uwsgi --emperor /app/uwsgi_sites/
