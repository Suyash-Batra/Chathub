import os
from pathlib import Path
import dj_database_url
from celery.schedules import crontab
import pymysql

pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent

# Detect if we are running on Render
IS_RENDER = 'RENDER' in os.environ

# --- SECURITY ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-local-fallback-key')
DEBUG = not IS_RENDER  # Automatically False on Render (Production), True locally

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# --- APPS CONFIGURATION ---
INSTALLED_APPS = [
    'cloudinary_storage',  # MUST be above staticfiles
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',  # Usually placed here

    # Third party apps
    'rest_framework',
    'encrypted_model_fields',
    'channels',
    'django_celery_beat',
    'corsheaders',

    # Local apps
    'base.apps.BaseConfig',
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

FIELD_ENCRYPTION_KEY = os.environ.get('FIELD_ENCRYPTION_KEY', 'CeLRe--mWN5UJ_Zp9-Hzht5ixsZAwJyiUqZzw8KqHGA=')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'studybud.urls'

# --- DATABASE ---
if IS_RENDER:
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }
    if 'default' in DATABASES:
        db_opts = DATABASES['default'].setdefault('OPTIONS', {})
        if any(k in db_opts for k in ['ssl-mode', 'ssl_mode']):
            db_opts['ssl'] = {'ca': None}
            db_opts.pop('ssl-mode', None)
            db_opts.pop('ssl_mode', None)
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'chathub_db'),
            'USER': 'root',
            'PASSWORD': 'pass123',
            'HOST': 'db',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

# --- REDIS & CHANNELS ---
REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/1')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [REDIS_URL]},
    },
}

# --- CELERY ---
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = None
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# --- TEMPLATES ---
TEMPLATES = [{
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
}]

# --- STATIC & MEDIA ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- SECURITY SETTINGS ---
CSRF_TRUSTED_ORIGINS = ["https://chathub-72tx.onrender.com"]
if not IS_RENDER:
    CSRF_TRUSTED_ORIGINS.append("http://localhost:8000")

CSRF_COOKIE_SECURE = IS_RENDER
SESSION_COOKIE_SECURE = IS_RENDER

WSGI_APPLICATION = 'studybud.wsgi.application'
ASGI_APPLICATION = 'studybud.asgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if IS_RENDER:
    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.StaticFilesStorage", # <--- CHANGE THIS LINE
        },
    }
