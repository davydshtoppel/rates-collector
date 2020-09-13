#!/usr/bin/env bash

python manage.py migrate --no-input

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
  python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '', '$DJANGO_SUPERUSER_PASSWORD')"
fi

gunicorn ecbrates.wsgi:application --bind 0.0.0.0:8000
