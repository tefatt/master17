"""
Django settings for untitled project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# import pymysql
#
# pymysql.install_as_MySQLdb()  # hack

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*7(p#%quqc4@vyr$2cpj)4&fak_3)h+5mdm+*&u5lwh)k$gk^n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'e_container',
    'rest_framework',
    'rest_framework.authtoken'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'e_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'e_core.wsgi.application'

# GOOGLE
# GOOGLE_API = {
#     'CLIENT_ID': '493593414963-snd1im5a0k54mtv89ol193igp0bej339.apps.googleusercontent.com',
#     'CLIENT_SECRET': 'w9H9FgJb8WQXfuxMKHfIt-Pu',
#     'SCOPE': ' '.join([
#         'profile',
#         'email',
#         'https://www.googleapis.com/auth/gmail.modify',
#         'https://www.googleapis.com/auth/gmail.readonly',
#         'https://www.googleapis.com/auth/gmail.compose',
#         'https://www.googleapis.com/auth/plus.me',
#         'https://www.googleapis.com/auth/contacts.readonly',
#         'https://www.googleapis.com/auth/drive.readonly',
#         'https://www.googleapis.com/auth/pubsub',
#         'https://www.googleapis.com/auth/calendar'
#     ]),
#     'PUSH_ENDPOINT': 'https://test.getunbox.com/api/services/notifications/',
#     'PROJECT': 'unbox2-174713',
#     'TOPIC': 'projects/unbox2-174713/topics/user-notifications'
# }


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eContainer',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',  # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'e_container',
#         'USER': 'root',
#         'PASSWORD': 'tempus993',
#         'HOST': '127.0.0.1',  # Or an IP Address that your DB is hosted on
#         'PORT': '3306',
#         'OPTIONS': {'charset': 'utf8mb4'},
#     },
#     'time_series': {
#         'ENGINE': 'django_mongodb_engine',
#         'NAME': 'my_database'
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'