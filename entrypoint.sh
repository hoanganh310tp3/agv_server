#!/bin/bash

# Wait for database to be ready
while ! nc -z db 5432; do
  echo "Waiting for postgres..."
  sleep 0.1
done

echo "PostgreSQL started"

# Run migrations
python manage.py migrate

# Create superuser if needed (optional)
# python manage.py createsuperuser --noinput

# Start server
exec "$@" 