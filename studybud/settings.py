import os
from pathlib import Path

import dj_database_url
from celery.schedules import crontab
import pymysql
pymysql.install_as_MySQLdb()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-(w7vo0xlbd5fl9g*^7_...')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Change this from ['127.0.0.1', 'localhost']
ALLOWED_HOSTS = [
    'chathub-72tx.onrender.com', 
    '127.0.0.1', 
    'localhost'
]

# Better yet, use the Render Environment Variable:
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'encrypted_model_fields',
    'channels',
    'django_celery_beat',
    'corsheaders',
    
    # Local apps
    'base.apps.BaseConfig',
]

FIELD_ENCRYPTION_KEY = 'CeLRe--mWN5UJ_Zp9-Hzht5ixsZAwJyiUqZzw8KqHGA='

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Best placed here for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'studybud.urls'

# --- REDIS & CHANNELS CONFIG ---
# Using 127.0.0.1 explicitly to avoid IPv6/localhost resolution delays
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/1')
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL], # Uses the dynamic URL
            "capacity": 1500,
            "expiry": 60,
        },
    },
}
CELERY_TASK_TIME_LIMIT = 120  # 2 minutes max
CELERY_TASK_SOFT_TIME_LIMIT = 90

# --- CELERY CONFIG ---
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = None  # We use the DB for results, keeps Redis light
CELERY_TASK_IGNORE_RESULT = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

CELERY_BEAT_SCHEDULE = {
    'auto-delete-expired-messages': {
        'task': 'base.tasks.delete_expired_messages', 
        'schedule': crontab(minute='*/10'),          
    },
}
# --- APPLICATION PATHS ---
WSGI_APPLICATION = 'studybud.wsgi.application'
ASGI_APPLICATION = 'studybud.asgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# --- DATABASE (MySQL/TiDB) ---
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# TiDB Cloud + PyMySQL SSL Handshake
if 'OPTIONS' in DATABASES['default']:
    opts = DATABASES['default']['OPTIONS']
    # Check for both dash and underscore versions from the URL query params
    if any(k in opts for k in ['ssl-mode', 'ssl_mode']):
        # PyMySQL requires the 'ssl' key to be a dictionary
        opts['ssl'] = {'ca': None}
        # Purge the keys that cause 'Unexpected Keyword Argument' errors
        opts.pop('ssl-mode', None)
        opts.pop('ssl_mode', None)
# --- AUTH & VALIDATION ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- STATIC & MEDIA ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Ensure Media directory exists
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True

if not DEBUG:
    CSRF_TRUSTED_ORIGINS = [f"https://{RENDER_EXTERNAL_HOSTNAME}"]
