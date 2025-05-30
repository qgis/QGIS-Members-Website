
"""Configuration for production server."""
# noinspection PyUnresolvedReferences
from .prod import *  # noqa
import ast
import os

DEBUG = False

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://*.qgis.org']

ADMINS = (
    # ('Dimas Ciputra', 'dimas@kartoza.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USERNAME'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': 5432,
        'TEST': {
            'NAME': 'unittests',
        }
    }
}


EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get(
    'EMAIL_HOST', 'smtp.resend.com')
EMAIL_HOST_USER = os.environ.get(
    'EMAIL_HOST_USER', 'automation@qgis.org')
EMAIL_HOST_PASSWORD = os.environ.get(
    'EMAIL_HOST_PASSWORD', 'your_resend_api_key')
EMAIL_PORT = os.environ.get(
    'EMAIL_PORT', '587')
EMAIL_SUBJECT_PREFIX = os.environ.get(
    'EMAIL_SUBJECT_PREFIX', '[QGIS Sustaining Members]')
EMAIL_USE_TLS = ast.literal_eval(os.environ.get(
    'EMAIL_USE_TLS', 'True'))
EMAIL_USE_SSL = ast.literal_eval(os.environ.get(
    'EMAIL_USE_SSL', 'False'))

