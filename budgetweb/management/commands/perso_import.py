from django.contrib.auth.models import User, Group
from django.core.management.base import NoArgsCommand
from django.core.management import call_command
from django.conf import settings


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        User.objects.create_superuser(
            'thierry.schlecht', 'thierry.schlecht@unistra.fr', '!')
        User.objects.create_superuser(
            'ludovic.hutin', 'ludovic.hutin@unistra.fr', '!')
        call_command('initial_import')

        # Ajout de ces utilisateurs au groupe DFI.
        liste_users = ['b.edel', 'caroline.wolff', 'aurelie.regnier',
                       'sylvie.siclerc', 'herve.heusser', 'f.idrissi.serh1',
                       'annie.spinella', 'g.weyrich', 'a.lauffenburger',
                       'norberti', 'hering']
        g = Group.objects.get(name=settings.DFI_GROUP_NAME)
        for u in liste_users:
            print(u)
            g.user_set.add(User.objects.get(username=u))
