from os import environ

from .dev import *

INTERNAL_IPS += ('172.16.240.1', )
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['*']

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
MIDDLEWARE_CLASSES += ()
