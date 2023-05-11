from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand
from django.core.management import call_command


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        User.objects.create_superuser(
            'myuser', 'myuser@my.little.poney.fr', '!')
        call_command('initial_import')
