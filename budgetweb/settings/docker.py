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
        'HOST': environ.get('POSTGRES_PORT_5432_TCP_ADDR', 'db'),
        'PORT': '5432',
    }
}
