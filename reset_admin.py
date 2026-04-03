import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studybud.settings')
django.setup()

from django.contrib.auth.models import User

# Replace 'admin' with your actual username if it's different
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'Suyash')
password = 'Meow' # You can change this here or use an Env Var

try:
    u = User.objects.get(username=username)
    u.set_password(password)
    u.save()
    print(f"Successfully reset password for user: {username}")
except User.DoesNotExist:
    print(f"User {username} not found. Creating new superuser...")
    User.objects.create_superuser(username, 'admin@example.com', password)