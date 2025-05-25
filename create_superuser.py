import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelancehub.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
if not password:
    print("Error: DJANGO_SUPERUSER_PASSWORD environment variable not set.")
    sys.exit(1)

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', password)
    print("Superuser created.")
else:
    print("Superuser already exists.")
