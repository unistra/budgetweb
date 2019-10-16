# -*- coding: utf-8 -*-


import os
import sys

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'budgetweb.settings.unittest'
django.setup()

from django.conf import settings
from django.test.runner import DiscoverRunner
from django.test.utils import get_runner

"""
Run tests script
"""

test_runner = DiscoverRunner(pattern='test*.py', verbosity=2,
                             interactive=True, failfast=False)
TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(['budgetweb'])
sys.exit(failures)
