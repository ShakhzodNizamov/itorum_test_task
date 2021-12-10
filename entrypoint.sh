#! /bin/bash

python manage.py makemigrations --no-input

python manage.py migrate --no-input

python manage.py collectstatic --no-input

exec gunicorn itorum_test_project.wsgi:application -b 0.0.0.0:8000 --reload