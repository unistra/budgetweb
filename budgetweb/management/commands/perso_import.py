from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand
from django.core.management import call_command


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        User.objects.create_superuser(
            'thierry.schlecht', 'thierry.schlecht@unistra.fr', '!')
        call_command('initial_import')
