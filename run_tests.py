# -*- coding: utf-8 -*-


import os
import sys

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'budgetweb.settings.unittest'
django.setup()

from django.test.runner import DiscoverRunner


"""
Run tests script
"""

test_runner = DiscoverRunner(pattern='test*.py', verbosity=2,
                             interactive=True, failfast=False)

failures = test_runner.run_tests(['budgetweb'])
sys.exit(failures)
