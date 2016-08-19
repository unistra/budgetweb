from unittest.mock import Mock

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.test import TestCase
from django.test.client import Client

from budgetweb.decorators import is_ajax_get, is_authorized_structure
from budgetweb.exceptions import StructureUnauthorizedException
from budgetweb.models import PlanFinancement, StructureAuthorizations


class BaseDecoratorsTest(TestCase):

    fixtures = ['tests/structures.json', 'tests/planfinancements.json',
                'tests/structureauthorizations.json']

    def test_is_authorized_structure(self):
        # The save method is not called in the fixtures
        StructureAuthorizations.objects.get(pk=1).save()

        request = HttpRequest()
        request.user = User.objects.get(pk=100)
        function = Mock()
        function.__name__ = 'mock'
        decorated_fuction = is_authorized_structure(function)
        decorated_fuction(request, pfiid=56)  # PAIE7R101
        self.assertTrue(function.called)

    def test_is_unauthorized_structure(self):
        request = HttpRequest()
        request.user = User.objects.get(pk=100)
        function = Mock()
        function.__name__ = 'mock'
        decorated_fuction = is_authorized_structure(function)
        response = decorated_fuction(request, pfiid=26)  # ECP
        self.assertFalse(function.called)
        self.assertEqual(
            response.content,
            StructureUnauthorizedException().message.encode('utf-8'))

    def test_is_ajax_get(self):

        """ test the decorator is_ajax_get with mock """
        request = HttpRequest()
        request.method = 'GET'
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        function = Mock()
        function.__name__ = 'mock'
        decorated_fuction = is_ajax_get(function)
        decorated_fuction(request)
        self.assertTrue(function.called)

    def test_is_not_ajax_get(self):

        """ test the decorator is_ajax_get with mock """
        request = HttpRequest()
        request.method = 'GET'
        function = Mock()
        function.__name__ = 'mock'
        decorated_fuction = is_ajax_get(function)
        with self.assertRaises(PermissionDenied):
            decorated_fuction(request)
        self.assertFalse(function.called)
