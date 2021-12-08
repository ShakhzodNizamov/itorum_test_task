#! /bin/bash

pyhon manage.py makemigrations --no-input

pyhon manage.py migrate --no-input

python manage.py collectstatic

exec gunicorn itorum_test_project.wsgi:application -b 0.0.0.0:8000 --reload