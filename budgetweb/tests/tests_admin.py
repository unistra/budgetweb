from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from budgetweb.admin import StructureAuthorizationsAdmin
from budgetweb.models import Structure, StructureAuthorizations


class MockRequest(object):
    pass


request = MockRequest()


class StructureAuthorizationsAdminTest(TestCase):

    fixtures = ['tests/structures.json']

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            'admin', email='admin@unistra.fr', password='pass')

    def tearDown(self):
        self.client.logout()

    def test_authorizations_add(self):
        # https://github.com/django/django/blob/1.8.14/tests/admin_views/tests.py#L203
        self.client.login(username='admin', password='pass')
        user = User.objects.create_user('user', password='pass')
        structure_paie = Structure.objects.get(code='PAIE')

        post_data = {
            "user": user.pk,
            "structures": [structure_paie.pk],
            "_save": "Save",
        }
        response = self.client.post(
            reverse('admin:budgetweb_structureauthorizations_add'),
            post_data, follow=True
        )

        authorized = user.structureauthorizations.structures.all()
        self.assertEqual(len(authorized), 4)
        self.assertListEqual(
            [structure.code for structure in authorized], 
            ['PAIE', 'PAIE7DIN', 'PAIE7ECP', 'PAIE7R101']
        )


class StructureAuthorizationsFormTest(TestCase):

    def test_tree(self):
        structure1 = Structure.objects.create(type='S', code='S1', label='S1')
        structure2 = Structure.objects.create(
            type='S', code='S2', label='S2', parent=structure1)
        structure3 = Structure.objects.create(
            type='S', code='S3', label='S3', parent=structure2)

        saa = StructureAuthorizationsAdmin(StructureAuthorizations, AdminSite())
        sa_form = saa.get_form(request)()
        choices = sa_form.fields['structures'].choices
        self.assertListEqual(
            [choice[1] for choice in choices], ['S1', '-- S2', '---- S3'])
