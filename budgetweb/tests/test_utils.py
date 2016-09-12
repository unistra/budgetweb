from django.contrib.auth.models import User
from django.test import TestCase

from budgetweb.models import Structure
from budgetweb.utils import get_authorized_structures_ids, get_current_year


class UtilsTest(TestCase):

    fixtures = [
        'tests/structures.json', 'tests/periodebudgets.json',
        'tests/structureauthorizations.json'
    ]

    def test_get_current_year(self):
        self.assertEqual(get_current_year(), 2017)

    def test_get_authorized_structures_ids(self):
        user = User.objects.get(pk=100)
        self.assertSetEqual(
            get_authorized_structures_ids(user)[0], {4})

    def test_get_authorized_structures_ids_with_hierarchy(self):
        user = User.objects.get(pk=100)
        self.assertSetEqual(
            get_authorized_structures_ids(user)[1], {4, 1})

    def test_get_authorized_structures_superuser(self):
        admin_user = User.objects.create_superuser(
            'admin', email='admin@unistra.fr', password='pass')
        active_structures = Structure.objects.filter(is_active=True)
        self.assertEqual(
            len(get_authorized_structures_ids(admin_user)[0]),
            len(active_structures)
        )
