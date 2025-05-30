# coding=utf-8

"""Project level settings.

Adjust these values as needed but don't commit passwords etc. to any public
repository!
"""

import os  # noqa
from django.utils.translation import gettext_lazy as _
from .utils import absolute_path
from .contrib import *  # noqa
import json

# Project apps
INSTALLED_APPS += [
    'base',
    'changes',
]

# Due to profile page does not available,
# this will redirect to home page after login
LOGIN_REDIRECT_URL = '/'

# How many versions to list in each project box
PROJECT_VERSION_LIST_SIZE = 10

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

SOUTH_TESTS_MIGRATE = False


# Set languages which want to be translated
LANGUAGES = (
    ('en', _('English')),
    ('id', _('Indonesian')),
)

# Set storage path for the translation files
LOCALE_PATHS = (absolute_path('locale'),)


MIDDLEWARE += [
    # For nav bar generation
    'core.custom_middleware.NavContextMiddleware',
    # Allauth middleware
    'allauth.account.middleware.AccountMiddleware'
]

# Project specific javascript files to be pipelined
# For third party libs like jquery should go in contrib.py
PIPELINE['JAVASCRIPT']['project'] = {
    'source_filenames': (
        'js/csrf-ajax.js',
        'js/form.js',
    ),
    'output_filename': 'js/project.js',
}

VALID_DOMAIN = json.loads(os.environ.get("VALID_DOMAIN", "[]"))

EMAIL_HOST_USER = 'noreply@kartoza.com'
LOGIN_URL = '/en/accounts/login/'

# The numeric mode (i.e. 0o644) to set newly uploaded files to.
FILE_UPLOAD_PERMISSIONS = 0o644


# Default primary key type
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'