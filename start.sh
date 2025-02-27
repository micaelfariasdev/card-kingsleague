#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn seu_projeto.wsgi:application --bind 0.0.0.0:$PORT
