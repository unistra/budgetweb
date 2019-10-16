# -*- coding: utf-8 -*-

from os import environ
from os.path import normpath
from .base import *

#######################
# Debug configuration #
#######################

DEBUG = True


##########################
# Database configuration #
##########################

# In your virtualenv, edit the file $VIRTUAL_ENV/bin/postactivate and set
# properly the environnement variable defined in this file (ie: os.environ[KEY])
# ex: export DEFAULT_DB_NAME='project_name'

# Default values for default database are :
# engine : sqlite3
# name : PROJECT_ROOT_DIR/default.db

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'budgetweb',
        'USER': 'budgetweb',
        'PASSWORD': 'budgetweb',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

#####################
# Log configuration #
#####################

LOGGING['handlers']['file']['filename'] = environ.get('LOG_DIR',
        normpath(join('/tmp', '%s.log' % SITE_NAME)))
LOGGING['handlers']['file']['level'] = 'DEBUG'

for logger in LOGGING['loggers']:
    LOGGING['loggers'][logger]['level'] = 'DEBUG'


###########################
# Unit test configuration #
###########################

INSTALLED_APPS += (
    'coverage',
)
#TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'

############
# Dipstrap #
############

DIPSTRAP_VERSION = environ.get('DIPSTRAP_VERSION', 'latest')
DIPSTRAP_STATIC_URL += '%s/' % DIPSTRAP_VERSION

#################
# Debug toolbar #
#################

DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS += ('172.16.240.1', )
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['*']

#################
# Interfaces SI #
#################

SIFACWS_DESC = 'https://FIXIT/sifacws/description.json'
SIFACWS_URL = 'https://FIXIT/'
SIFACWS_APIKEY = 'FIXIT'
