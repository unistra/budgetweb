# -*- coding: utf-8 -*-

from os import environ
from os.path import normpath
from .dev import *

#######################
# Debug configuration #
#######################

DEBUG = True


##########################
# Database configuration #
##########################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get('DEFAULT_DB_TEST_NAME', 'budgetweb'),
        'USER': environ.get('DEFAULT_DB_TEST_USER', 'budgetweb'),
        'PASSWORD': environ.get('DEFAULT_DB_TEST_PASSWORD', 'budgetweb'),
        'HOST': environ.get('DEFAULT_DB_TEST_HOST', 'postgres'),
        'PORT': environ.get('DEFAULT_DB_TEST_PORT', ''),
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
