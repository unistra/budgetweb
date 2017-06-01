from datetime import datetime, timedelta
from unittest.mock import Mock

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.test import TestCase

from budgetweb.decorators import (is_ajax_get, is_authorized_editing,
                                  is_authorized_structure)
from budgetweb.exceptions import (
    EditingUnauthorizedException, PeriodeBudgetUninitializeError,
    StructureUnauthorizedException)
from budgetweb.models import (PeriodeBudget, PlanFinancement, Structure,
                              StructureAuthorizations)


class BaseDecoratorsTest(TestCase):

    fixtures = ['tests/structures', 'tests/planfinancements',
                'tests/structureauthorizations']

    def test_is_authorized_structure_by_pfiid(self):
        # The save method is not called in the fixtures
        StructureAuthorizations.objects.get(pk=1).save()

        request = HttpRequest()
        request.user = User.objects.get(pk=100)
        function = Mock()
        function.__name__ = 'mock'
        decorated_fuction = is_authorized_structure(function)
        pfi = PlanFinancement.objects.get(structure__code='PAIE7R101')
        decorated_fuction(request, pfiid=pfi.pk)
        self.assertTrue(function.called)

    def test_is_authorized_structure_by_structid(self):
        # The save method is not called in the fixtures
        StructureAuthorizations.objects.get(pk=1).save()

        request = HttpRequest()
        request.user = User.objects.get(pk=100)
        function = Mock()
        function.__name__ = 'mock'
        decorated_fuction = is_authorized_structure(function)
        structure = Structure.objects.get(code='PAIE7R101')
        decorated_fuction(request, structid=structure.pk)
        self.assertTrue(function.called)

    def test_is_unauthorized_structure(self):
        request = HttpRequest()
        request.user = User.objects.get(pk=100)
        function = Mock()
        function.__name__ = 'mock'
        decorated_fuction = is_authorized_structure(function)
        pfi = PlanFinancement.objects.get(structure__code='ECP')
        response = decorated_fuction(request, pfiid=pfi.pk)
        self.assertFalse(function.called)
        self.assertEqual(
            response.content,
            StructureUnauthorizedException().message.encode('utf-8'))

    def test_is_unauthorized_structure_no_parameters(self):
        request = HttpRequest()
        request.user = User.objects.get(pk=100)
        function = Mock()
        function.__name__ = 'mock'
        decorated_fuction = is_authorized_structure(function)
        response = decorated_fuction(request)
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


class IsAuthorizedEditingTest(TestCase):

    fixtures = ['tests/structures', 'tests/structureauthorizations']

    def test_no_dates_configured(self):
        PeriodeBudget.objects.create(period_id=1, annee=2017)
        request = HttpRequest()
        request.user = User.objects.get(pk=100)
        function = Mock()
        function.__name__ = 'mock'
        decorated_fuction = is_authorized_editing(function)
        response = decorated_fuction(request)
        self.assertFalse(function.called)
        self.assertEqual(
            response.content,
            PeriodeBudgetUninitializeError().message.encode('utf-8'))

    def test_editing_unauthorized(self):
        begin_date = datetime.today() + timedelta(days=1)
        end_date = begin_date + timedelta(days=2)
        PeriodeBudget.objects.create(
            period_id=1, annee=2017, date_debut_saisie=begin_date,
            date_fin_saisie=end_date, date_debut_retardataire=begin_date,
            date_fin_retardataire=end_date, date_debut_dfi=begin_date,
            date_fin_dfi=end_date, date_debut_admin=begin_date,
            date_fin_admin=end_date)

        request = HttpRequest()
        request.user = User.objects.get(pk=100)
        function = Mock()
        function.__name__ = 'mock'
        decorated_fuction = is_authorized_editing(function)
        response = decorated_fuction(request)
        self.assertFalse(function.called)
        self.assertEqual(
            response.content,
            EditingUnauthorizedException().message.encode('utf-8'))

    def test_valid_input_dates(self):
        begin_date = datetime.today()
        end_date = begin_date + timedelta(days=1)
        PeriodeBudget.objects.create(
            period_id=1, annee=2017, date_debut_saisie=begin_date,
            date_fin_saisie=end_date, date_debut_retardataire=begin_date,
            date_fin_retardataire=end_date, date_debut_dfi=begin_date,
            date_fin_dfi=end_date, date_debut_admin=begin_date,
            date_fin_admin=end_date)

        request = HttpRequest()
        request.user = User.objects.get(pk=100)
        function = Mock()
        function.__name__ = 'mock'
        decorated_fuction = is_authorized_editing(function)
        decorated_fuction(request)
        self.assertTrue(function.called)

    def test_valid_input_dates_late_group(self):
        begin_date = datetime.today()
        end_date = begin_date + timedelta(days=1)
        other_date = begin_date + timedelta(days=100)
        PeriodeBudget.objects.create(
            period_id=1, annee=2017, date_debut_saisie=other_date,
            date_fin_saisie=other_date, date_debut_retardataire=begin_date,
            date_fin_retardataire=end_date, date_debut_dfi=begin_date,
            date_fin_dfi=end_date, date_debut_admin=begin_date,
            date_fin_admin=end_date)

        request = HttpRequest()
        user = User.objects.get(pk=100)
        late_group = Group.objects.create(name=settings.LATE_GROUP_NAME)
        user.groups.add(late_group)

        request.user = user
        function = Mock()
        function.__name__ = 'mock'
        decorated_fuction = is_authorized_editing(function)
        decorated_fuction(request)
        self.assertTrue(function.called)

    def test_valid_input_dates_dfi_group(self):
        begin_date = datetime.today()
        end_date = begin_date + timedelta(days=1)
        other_date = begin_date + timedelta(days=100)
        PeriodeBudget.objects.create(
            period_id=1, annee=2017, date_debut_saisie=other_date,
            date_fin_saisie=other_date, date_debut_retardataire=begin_date,
            date_fin_retardataire=end_date, date_debut_dfi=begin_date,
            date_fin_dfi=end_date, date_debut_admin=begin_date,
            date_fin_admin=end_date)

        request = HttpRequest()
        user = User.objects.get(pk=100)
        dfi_group = Group.objects.create(name=settings.DFI_GROUP_NAME)
        user.groups.add(dfi_group)

        request.user = user
        function = Mock()
        function.__name__ = 'mock'
        decorated_fuction = is_authorized_editing(function)
        decorated_fuction(request)
        self.assertTrue(function.called)

    def test_valid_input_dates_superuser(self):
        begin_date = datetime.today()
        end_date = begin_date + timedelta(days=1)
        other_date = begin_date + timedelta(days=100)
        PeriodeBudget.objects.create(
            period_id=1, annee=2017, date_debut_saisie=other_date,
            date_fin_saisie=other_date, date_debut_retardataire=begin_date,
            date_fin_retardataire=end_date, date_debut_dfi=begin_date,
            date_fin_dfi=end_date, date_debut_admin=begin_date,
            date_fin_admin=end_date)

        request = HttpRequest()
        user = User.objects.get(pk=100)
        user.is_superuser = True
        user.save()

        request.user = user
        function = Mock()
        function.__name__ = 'mock'
        decorated_fuction = is_authorized_editing(function)
        decorated_fuction(request)
        self.assertTrue(function.called)
