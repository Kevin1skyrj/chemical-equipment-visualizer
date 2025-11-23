#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Ensure superuser exists with the provided credentials
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
    python manage.py ensure_superuser --username "$DJANGO_SUPERUSER_USERNAME" --password "$DJANGO_SUPERUSER_PASSWORD" --email "$DJANGO_SUPERUSER_EMAIL"
else
    echo "Skipping ensure_superuser (missing DJANGO_SUPERUSER_* env vars)."
fi
