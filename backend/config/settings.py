import os
from pathlib import Path

import environ

#build path
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()

#Read .env file
env_file = os.path.join (BASE_DIR, '.env')
if os.path.exists(env_file):
    env.read_env(env_file)

#Security warning: keep the secret key used in production secret!
SECRET_KEY = env ('secret_key', default='insecure-dev-key-change-production')

#Secret Warning: don't run with debug turned on in production
DEBUG = env.bool('DEBUG', defaulet=False)


ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

#Third party apps
    'corsheaders',
    'health_check',
    'health_check.db',
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.redis'
    'django_celery_beat',
    'django_celery.results',

#Local apps

    'apps.accounts'
    'apps.quiz'
    'apps.core'


    ]

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'withenoise.middleware.WithNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib,auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.SessionMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.core.middlewareRateLimitMiddleware',
    'apps.core.middleware.RequestLogMiddleware',

]
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.templates.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.templates.context.processors.debug',
                'django.templates.context.processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        }
    }
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backend.postgresql',
        'NAME': env('DB_NAME', defualt='quizdb'),
        'USER': env('DB_USER', default='quizuser'),
        'PASSWORD': env('DB_PASSWORD', defualt='quizpass'),
        'HOST': env('DB_HOST', defualt='localhost'),
        'PORT': env('DB_PORT', defualt = '5432'),
        'CONN_MAX_AGE': 60,
        'OPTIONS':{
            'connect_timeout': 10

        }

    }
}

# redis cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://:{env('REDIS_PASSWORD')}@{env('REDIS_HOST')}:{env('REDIS_PORT', default='6379')}/0",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTIONS_POOL_CLASS_KWARGS':{
                'max_connections': 50,
                'timeout': 20,

            },
            'MAX_CONNECTIONS': 1000,
            'PICKLE_VERSION': 1,

        },
        'KEY_PREFIX': 'quiz',
        'TIMEOUT': 300,

    }
}