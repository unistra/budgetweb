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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%s' 
            % environ.get('DEFAULT_DB_TEST_ENGINE', 'sqlite3'),
        'NAME': environ.get('DEFAULT_DB_TEST_NAME', 'budgetweb.db'),
        'USER': environ.get('DEFAULT_DB_TEST_USER'),
        'PASSWORD': environ.get('DEFAULT_DB_TEST_PASSWORD'),
        'HOST': environ.get('DEFAULT_DB_TEST_HOST'),
        'PORT': '5432',
    },
}


#####################
# Log configuration #
#####################

LOGGING['handlers']['file']['filename'] = environ.get('LOG_DIR',
        normpath(join('/tmp', 'test_%s.log' % SITE_NAME)))
LOGGING['handlers']['file']['level'] = 'DEBUG'

for logger in LOGGING['loggers']:
    LOGGING['loggers'][logger]['level'] = 'DEBUG'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
