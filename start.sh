#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn project.wsgi:application --bind 0.0.0.0:$PORT
