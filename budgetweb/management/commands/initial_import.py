from os.path import dirname, join

from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.core.management import call_command


class Command(NoArgsCommand):
    help = 'Initial import for BudgetWeb'

    def handle_noargs(self, **options):
        datapath = join(settings.SITE_ROOT, 'datas')

        try:
            print('***** Import structures *****')
            call_command('import_structures', join(datapath, 'structures.csv'))
            print('***** Import functional domains *****')
            call_command('import_functionaldomains',
                         join(datapath, 'domaines_fonctionnels.csv'))
            print('***** Import NatudeComptableDepense *****')
            call_command('import_naturecomptabledepense',
                         join(datapath, 'naturecomptabledepense.csv'))
            print('***** Import NatudeComptableRecette *****')
            call_command('import_naturecomptablerecette',
                         join(datapath, 'naturecomptablerecette.csv'))
            print('***** Import Financial Plans *****')
            #call_command('import_pfi',
            #             join(datapath, 'planfinancement.csv'))
            print('***** Import PeriodeBudget *****')
            call_command('import_periodebudget')

        except Exception as e:
            print(e)
