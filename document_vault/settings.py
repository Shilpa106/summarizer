"""
Django settings for document_vault project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os
import dj_database_url
import django_heroku
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ke0bv97*-wh=ehi=4(stnv*%i^@(toxk2jfuncxfxx+$e)a0ap'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['ec2-52-59-213-57.eu-central-1.compute.amazonaws.com:8000', '172.31.39.128:8000']

#User Model

AUTH_USER_MODEL = 'Users.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'Users.apps.UsersConfig',
    'Subscription.apps.SubscriptionConfig',
    'DocumentFeature.apps.DocumentfeatureConfig',
    'DocumentUpload.apps.DocumentuploadConfig',

    'drf_yasg',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
]

MIDDLEWARE = [
    'middlewares.request_middleware.RequestMiddleware',
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

ROOT_URLCONF = 'document_vault.urls'


# Allow corse headers

CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://127.0.0.1:8000",
#     "http://127.0.0.1:3000",
# ]


REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False, # To show all the decimal value in decimal not str
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    )
}


# Token Life Setting 
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'document_vault.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# DEBUG = config('DEBUG', default=True, cast=bool)
# DATABASES = {
#     'default': dj_database_url.config(
#         default=config('DATABASE_URL')
#     )
# }



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# GDrive File Upload Settings
GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = 'GoogleDriveUpload-027e9d367d8f.json'
GOOGLE_DRIVE_STORAGE_MEDIA_ROOT = '16L081recrstgjYnfa8PhZu6prNbVdj-p?usp=sharing'
FOLDER_ID = '16L081recrstgjYnfa8PhZu6prNbVdj-p'
SCOPES = ['https://www.googleapis.com/auth/drive']
PERMISSION1 = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': 'globalkhabariabdulla@gmail.com',  # Please set your email of Google account.
            }
PERMISSION2 = {
            'type': 'anyone',
            'role': 'reader',
            }




EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'globalkhabariabdulla@gmail.com'
EMAIL_HOST_PASSWORD = 'Sameer783@'


django_heroku.settings(locals())
