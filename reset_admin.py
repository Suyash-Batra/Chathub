import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studybud.settings')
django.setup()

from django.contrib.auth.models import User

# Get credentials from Render Environment Variables
username = os.environ.get('ADMIN_USERNAME', 'admin')
password = os.environ.get('ADMIN_PASSWORD')

if not password:
    print("Error: ADMIN_PASSWORD environment variable not set!")
else:
    try:
        u = User.objects.get(username=username)
        u.set_password(password)
        u.save()
        print(f"✅ Password successfully reset for: {username}")
    except User.DoesNotExist:
        print(f"User {username} not found. Creating new superuser...")
        User.objects.create_superuser(username, 'admin@example.com', password)