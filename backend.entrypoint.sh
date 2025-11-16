#!/bin/sh

set -e


# Deine originalen Befehle (ohne wait_for_db)
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
# python manage.py test

# Create a superuser using environment variables
# (Dein Superuser-Erstellungs-Code bleibt gleich)
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser '{username}'...")
    # Korrekter Aufruf: username hier übergeben
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created.")
else:
    print(f"Superuser '{username}' already exists.")

guest_username = 'max'
guest_email = 'max@example.com'
guest_password = 'IhrPasswort123'

if not User.objects.filter(username=guest_username).exists():
    print(f"Creating guest user '{guest_username}'...")
    User.objects.create_user(username=guest_username, email=guest_email, password=guest_password, first_name='Max', last_name='Mustermann')
    print(f"Guest user '{guest_username}' created.")
else:
    print(f"Guest user '{guest_username}' already exists.")
EOF



exec gunicorn core.wsgi:application --bind 0.0.0.0:8000
