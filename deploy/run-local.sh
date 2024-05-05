#!/bin/sh
until pg_isready -h db; do echo "waiting for postgres..."  && sleep 0.5; done
python manage.py migrate
while true; do python manage.py runserver 0.0.0.0:8000 && sleep 1; done
