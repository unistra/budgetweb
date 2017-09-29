from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import TestCase

from budgetweb.models import PeriodeBudget


class PeriodYearsContextProcessorTest(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            'admin', email='admin@unistra.fr', password='pass')
        self.client.login(username='admin', password='pass')

    def tearDown(self):
        self.client.logout()

    def test_without_periods(self):
        ctx = self.client.get('/showtree/gbcp/')
        self.assertListEqual(list(ctx.context['period_years']), [])

    def test_empty_session_value(self):
        PeriodeBudget.objects.create(period_id=1, annee=2017)
        PeriodeBudget.objects.create(period_id=1, annee=2018, is_active=False)
        ctx = self.client.get('/showtree/gbcp/')
        self.assertListEqual(list(ctx.context['period_years']), [2018])

    def test_with_session_value(self):
        PeriodeBudget.objects.create(period_id=1, annee=2017)
        PeriodeBudget.objects.create(period_id=1, annee=2018, is_active=False)

        # Set the session
        session = self.client.session
        session['period_year'] = 2018
        session.save()

        ctx = self.client.get('/showtree/gbcp/')
        self.assertListEqual(list(ctx.context['period_years']), [2017])
