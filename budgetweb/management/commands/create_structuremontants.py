from contextlib import contextmanager
from decimal import Decimal
import multiprocessing as mp
import random

from django import db
from django.conf import settings
from django.core.management.base import BaseCommand

from budgetweb.models import (
    Depense, PeriodeBudget, Recette, StructureMontant)
from budgetweb.apps.structure.models import (
    DomaineFonctionnel, NatureComptableDepense, NatureComptableRecette,
    PlanFinancement)


NUMBER_ENTRIES = 100
PROCESS_ENTRIES = 25
MAX_MONTANT = 100000


def get_random_object(object_list, qs=None):
    if qs:
        object_list = object_list.filter(**qs)
    obj = object_list[random.randint(0, len(object_list) - 1)]
    return obj


@contextmanager
def temporary_settings(**temp_settings):
    is_sqlite = settings.DATABASES['default']['ENGINE'].endswith('sqlite3')
    if is_sqlite:
        base_options = settings.DATABASES['default']['OPTIONS']
        settings.DATABASES['default']['OPTIONS'].update({'timeout': 30})
    yield
    if is_sqlite:
        settings.DATABASES['default']['OPTIONS'] = base_options


class Command(BaseCommand):
    help = 'Creates random StructureMontant objects'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '-d', '--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete previous Recette, Depense and StructureMontant objects',
        )
        parser.add_argument(
            '-e',
            dest='number_entries',
            default=NUMBER_ENTRIES,
            help='Total number of created StuctureMontant',
        )
        parser.add_argument(
            '-p',
            dest='process_entries',
            default=PROCESS_ENTRIES,
            help='Number of created StuctureMontant by process',
        )

    def handle(self, *args, **options):
        if options['delete']:
            Recette.active_period.all().delete()
            Depense.active_period.all().delete()
            StructureMontant.active_period.all().delete()

        self.periodebudget = PeriodeBudget.active.first()
        self.domainefonctionnels = DomaineFonctionnel.active.all()
        self.naturecomptabledepenses = NatureComptableDepense.active.all()
        self.naturecomptablerecettes = NatureComptableRecette.active.all()
        self.pfis = PlanFinancement.active.all()
        self.number_entries = int(options['number_entries'])
        self.process_entries = int(options['process_entries'])

        index = 0
        jobs = []
        created = mp.Value('i', 0)

        # Prevents SSL Error with the database connection before fork
        db.close_old_connections()
        # with temporary_settings():
        while index < self.number_entries:
            end = min(self.number_entries, index + self.process_entries)
            p = mp.Process(
                target=self.worker_entry,
                name='montants_%s' % index,
                args=(index, end, created))
            jobs.append(p)
            p.start()

            index += self.process_entries

        for j in jobs:
            j.join()

        print('Objects created : %s' % created.value)

    def worker_entry(self, begin, end, created):
        for i in range(begin, end):
            pfi = get_random_object(self.pfis)
            domainefonctionnel = get_random_object(self.domainefonctionnels)
            structure = pfi.structure
            annee = self.periodebudget.annee
            naturecomptabledepense = get_random_object(
                self.naturecomptabledepenses, qs={'is_fleche': pfi.is_fleche})
            naturecomptablerecette = get_random_object(
                self.naturecomptablerecettes, qs={'is_fleche': pfi.is_fleche})

            data = (
                (Depense, {
                    'pfi': pfi,
                    'structure': structure,
                    'periodebudget': self.periodebudget,
                    'annee': annee,
                    'domainefonctionnel': domainefonctionnel,
                    'naturecomptabledepense': naturecomptabledepense,
                    'creepar': 'budgetweb'
                }),
                (Recette, {
                    'pfi': pfi,
                    'structure': structure,
                    'periodebudget': self.periodebudget,
                    'annee': annee,
                    'naturecomptablerecette': naturecomptablerecette,
                    'creepar': 'budgetweb',
                }),
            )

            for model, values in data:
                obj = model(**values)
                montants = obj.initial_montants
                value = Decimal(random.randrange(MAX_MONTANT * 100)) / 100
                for montant in montants:
                    setattr(obj, montant, value)
                obj.save()

            with created.get_lock():
                created.value += 1
