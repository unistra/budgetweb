from decimal import Decimal

from django.test import TestCase

from budgetweb.templatetags import budgetweb_tags as tags


class TemplatetagsTestCase(TestCase):

    def test_intspace(self):
        # With USE_L10N and string value
        # Remove the NO-BREAK SPACE character
        self.assertEqual(
            tags.intspace('1000000').replace('\xa0', ' '), '1 000 000')

        # With USE_L10N and incorrect string value
        self.assertEqual(tags.intspace('abcd'), 'abcd')

        # With USE_L10N and int value
        # Remove the NO-BREAK SPACE character
        self.assertEqual(
            tags.intspace(1000000).replace('\xa0', ' '), '1 000 000')

        # With USE_L10N and Decimal value
        # Remove the NO-BREAK SPACE character
        self.assertEqual(
            tags.intspace(Decimal(1000000.25)).replace('\xa0', ' '),
            '1 000 000,25')

        # With None value
        self.assertIsNone(tags.intspace(None))

        # Without USE_L10N and int value
        self.assertEqual(tags.intspace(1000000, False), '1 000 000')

        # Without USE_L10N and string value
        self.assertEqual(tags.intspace('1000000', False), '1 000 000')

    def test_dictvalue(self):
        value = {'a': 1, 'b': 2}
        self.assertEqual(tags.dictvalue(value, 'a'), 1)

    def test_resume_colspan(self):
        periodes1 = ('BI', 'Virement')
        periodes2 = ()
        montant_types = {'AE': 1, 'CP': 2}

        self.assertEqual(
            tags.resume_colspan(periodes1, periodes2, montant_types), 7)
