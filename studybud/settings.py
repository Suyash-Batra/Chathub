import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# 1. Load local .env if it exists
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Security & Environment
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

CSRF_TRUSTED_ORIGINS = [
    'https://chathub-72tx.onrender.com',
]

# While you're at it, ensure your Render URL is also in ALLOWED_HOSTS
ALLOWED_HOSTS = [
    'chathub-72tx.onrender.com',
    'localhost',
    '127.0.0.1',
]

# 3. Application definition
INSTALLED_APPS = [
    'daphne',  # Must be at the very top for Channels
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # For static files in dev
    'django.contrib.staticfiles',
    'base.apps.BaseConfig',
    'rest_framework',
    'encrypted_model_fields',
    'channels',
    # 'django_celery_beat',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # ✅ Fixed: Added comma
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'studybud.urls'

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

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
    )
}

# Only apply the Linux-specific SSL path if we are NOT on Windows
if DATABASES['default'].get('ENGINE') == 'django.db.backends.mysql':
    # If DATABASE_URL is present (usually on Render)
    if os.environ.get('DATABASE_URL'):
        # On Render/Linux, we need the CA path
        if os.name != 'nt':  # 'nt' means Windows
            DATABASES['default']['OPTIONS'] = {
                'ssl': {
                    'ca': '/etc/ssl/certs/ca-certificates.crt'
                }
            }
        else:
            # On Windows locally, TiDB usually works without the explicit 'ca' path
            # if your system certificates are up to date.
            DATABASES['default']['OPTIONS'] = {
                'ssl': {}
            }

# 5. Redis & Channels (Upstash)
REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    },
}

# 6. Celery (Upstash)
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# 7. Static Files (WhiteNoise)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
# Enables compression and caching support
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 8. Others
WSGI_APPLICATION = 'studybud.wsgi.application'
ASGI_APPLICATION = 'studybud.asgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True
FIELD_ENCRYPTION_KEY = os.environ.get('FIELD_ENCRYPTION_KEY', 'CeLRe--mWN5UJ_Zp9-Hzht5ixsZAwJyiUqZzw8KqHGA=')