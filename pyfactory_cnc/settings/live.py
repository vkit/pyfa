from base import *



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "excellence",
        'USER': "emiamar",
        'PASSWORD': "dklsjfawijr239jdkls12e",
        'HOST': "127.0.0.1",
    }
}


STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    (os.path.join(BASE_DIR, '../', 'static')),
]

MEDIA_ROOT = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__), '../../../../media/').replace('\\', '/'))
STATIC_ROOT = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__), '../../../../static/').replace('\\', '/'))
