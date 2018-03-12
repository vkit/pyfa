"""

Django settings for pyfactory_cnc project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0*$i6uj#)brv7_c55s=^4%4&*-5g8y=*ym8_**883hze*=7yc2'


ALLOWED_HOSTS = []


# Application definition


DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_extlog',
    'crispy_forms',
    'debug_toolbar'
]

CORE_APPS = [
    'base',
    'core',
    'app',
    'modeller',
    'sampleapp',
    'page',
    'authentication',
]

# Project apps base template dir used in authentication app

PROJECT_BASE_TEMPLATE_DIR = os.path.normpath(os.path.join(
    BASE_DIR, '../', 'templates', 'project_base'))

# Dynamically inserting app from project_directory

sys.path.insert(0, os.path.join(BASE_DIR, '../', '../', 'project_directory'))


PROJECT_APPS_DIR = os.path.normpath(os.path.join(
    BASE_DIR, '../', '../', 'project_directory'))


PROJECT_APPS = [
]


for item in os.listdir(PROJECT_APPS_DIR):
    if os.path.isfile(os.path.join(PROJECT_APPS_DIR, item, '__init__.py')):
        app_name = '%s' % item
        if app_name not in PROJECT_APPS:
            THIRD_PARTY_APPS.append(app_name)


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CORE_APPS + PROJECT_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_extlog.middleware.AuditLoggingMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'pyfactory_cnc.urls'

WSGI_APPLICATION = 'pyfactory_cnc.wsgi.application'

LOGIN_URL = '/'

LOGIN_REDIRECT_URL = '/dashboard_dispatcher/'


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

CRISPY_TEMPLATE_PACK = "bootstrap3"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.normpath(os.path.join(BASE_DIR, '../', 'templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'basic': {
            'format': '%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'basic',
            'filename': ('/home/raghu/staurday/edutech/logs/py_local.log'),
        },
    },
    'loggers': {
        'base': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True,

        },
        'core': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True,

        },
        'app': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True,

        },
        'project': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True,

        },
        'modeller': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True,

        },
        'routecard': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True,

        },
    }
}

