#!/usr/bin/env bash

python manage.py migrate --no-input

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
  python manage.py createsuperuser --no-input
fi

uwsgi --http :8000 --module ecbrates.wsgi