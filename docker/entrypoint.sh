#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 1
    done
    sleep 8
    echo "PostgreSQL started"
fi

# python manage.py flush --no-input
alembic upgrade head

exec "$@"