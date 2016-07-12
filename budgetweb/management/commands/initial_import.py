from os.path import dirname, join

from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.core.management import call_command


class Command(NoArgsCommand):
    help = 'Initial import for BudgetWeb'

    def handle_noargs(self, **options):
        datapath = join(settings.SITE_ROOT, 'datas')
        print('FF : %s' % datapath)

        try:
            print('***** Import structures *****')
            call_command('import_structures', join(datapath, 'structures.csv'))
            print('***** Import functional domains *****')
            call_command('import_functionaldomains',
                         join(datapath, 'domaines_fonctionnels.csv'))
        except Exception as e:
            print(e)
