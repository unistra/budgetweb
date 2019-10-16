from django.contrib.auth.models import User
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
        res = self.client.get('/showtree/gbcp/')
        self.assertListEqual(
            list(res.context['period_years']), [(2017, ' (BI)'), (2018, '')])

    def test_with_session_value(self):

        PeriodeBudget.objects.create(period_id=1, annee=2017)
        PeriodeBudget.objects.create(period_id=1, annee=2018, is_active=False)

        # Set the session
        session = self.client.session
        session['period_year'] = 2018
        session.save()

        res = self.client.get('/showtree/gbcp/')
        self.assertListEqual(
            list(res.context['period_years']), [(2018, ''), (2017, ' (BI)')])

    def test_with_existing_session_value(self):

        PeriodeBudget.objects.create(period_id=1, annee=2017)
        PeriodeBudget.objects.create(period_id=1, annee=2018, is_active=False)

        # Set the session
        session = self.client.session
        session['period_year'] = 2018
        session['current_period_year'] = 2018
        session['period_years'] = [(2018, ''), (2017, ' (BI)')]
        session.save()

        res = self.client.get('/showtree/gbcp/')
        self.assertListEqual(
            list(res.context['period_years']), [[2018, ''], [2017, ' (BI)']])
