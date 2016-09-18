import datetime
from decimal import Decimal
from itertools import groupby

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models, transaction
from django.db.models import F, Q, Sum
from django.utils.translation import ugettext_lazy as _

from .decorators import require_lock


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class ActivePeriodManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(periodebudget__is_active=True)


class StructureAuthorizations(models.Model):
    """
    Gestion des autorisations utilisateurs sur les CF
    Possibilités: * P* PAIE* ou un nom précis
    """
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL)
    structures = models.ManyToManyField('Structure',
                                        related_name='authorized_structures')

    class Meta:
        verbose_name = 'structure authorization'
        verbose_name_plural = 'structures authorizations'

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.pk:
            for structure in self.structures.all():
                for children in structure.get_children():
                    self.structures.add(children)
        super().save(*args, **kwargs)


class PeriodeBudget(models.Model):
    """
    Gestion des périodes de budget. Une seule active
    avec bloqué=False. Les dépenses et les recettes
    sont saisies pour une période
    """
    code = models.CharField('Libellé court', max_length=20)
    label = models.CharField('Libellé long', max_length=255)
    annee = models.PositiveIntegerField('Année')
    is_active = models.BooleanField('Activé (oui/,non)', default=True)

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return '{0.code} -- {0.label} -- {0.annee}'.format(self)


class DomaineFonctionnel(models.Model):
    """
    Gestion des domaines fonctionnels. En cours de précisions
    """
    code = models.CharField('Code', max_length=100, default="", unique=True)
    label = models.CharField('Libellé', max_length=255, default="")
    label_court = models.CharField('Libellé court', max_length=100, default="",
                                   null=True, blank=True,)
    is_active = models.BooleanField('Actif', max_length=100, default=True)

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return '{0.code} - {0.label_court}'.format(self)


class Structure(models.Model):
    """
    Gestion de la hiérarchie des Objets CF. En cours de précisions
    """
    code = models.CharField('Code', max_length=100, unique=True)
    label = models.CharField('Libellé', max_length=255)
    parent = models.ForeignKey(
        'Structure', blank=True, null=True, related_name='fils',
        verbose_name=u'Lien direct vers la structure parent')
    groupe1 = models.CharField('Groupe BudgetWeb 1', max_length=255,
                               blank=True, null=True)
    groupe2 = models.CharField('Groupe BudgetWeb 2', max_length=255,
                               blank=True, null=True)
    is_active = models.BooleanField('Actif', max_length=100, default=True)
    # Depth: 1 == root
    depth = models.PositiveIntegerField()
    # Path: /id_root/id_ancestor1/id_ancestor2/...
    path = models.TextField(_('Path'), blank=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ['code']

    def __str__(self):
        return '{0.code} - {0.label}'.format(self)

    def save(self, *args, **kwargs):
        parent = self.parent
        self.path = '{0.path}/{0.id}'.format(parent) if parent else ''
        self.depth = parent.depth + 1 if parent else 1
        super().save(*args, **kwargs)

    def get_ancestors(self):
        parent = self.parent
        return [parent] + parent.get_ancestors() if parent else []

    def get_children(self):
        children = []
        for sons in self.get_sons():
            children.append(sons)
            children.extend(sons.get_children())
        return children

    def get_unordered_children(self):
        return Structure.objects.filter(
            Q(path__contains='/%s/' % self.pk) | Q(parent_id=self.pk))

    def get_sons(self):
        return self.fils.filter(is_active=True).order_by('code')

    @property
    def full_path(self):
        return '{0.path}/{0.pk}'.format(self)

    def get_full_path(self, order=True):
        ids = self.full_path.split('/')[1:]
        structures = list(Structure.objects.filter(pk__in=ids))
        if order:
            structures.sort(key=lambda s: ids.index(str(s.pk)))
        return structures


class PlanFinancement(models.Model):
    """
    Gestion des Plans de financement. En cours de précisions
    """
    structure = models.ForeignKey('Structure',
                                  verbose_name='Lien direct vers le CF')
    code = models.CharField('Code du PFI', max_length=100, default='NA')
    label = models.CharField('Libellé', max_length=255)
    eotp = models.CharField("Code court de l'eotp", max_length=100)
    centrecoutderive = models.CharField('Centre de coût associé',
                                        max_length=100)
    centreprofitderive = models.CharField('Centre de profit associé',
                                          max_length=100)
    groupe1 = models.CharField('Groupe BudgetWeb 1', max_length=255,
                               null=True, blank=True)
    groupe2 = models.CharField('Groupe BudgetWeb 2', max_length=255,
                               null=True, blank=True)
    is_fleche = models.BooleanField('Fléché oui/non', default=False)
    is_pluriannuel = models.BooleanField('Pluriannuel oui/non', default=False)
    is_active = models.BooleanField('Actif', max_length=100, default=True)
    date_debut = models.DateField('Date de début', null=True, blank=True,
                                  help_text='Date de début')
    date_fin = models.DateField('Date de fin', null=True, blank=True,
                                help_text='Date de fin')

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ['label']

    def __str__(self):
        return '{0.code}'.format(self)

    # Retourne un tableau avec l'année, la
    #
    def get_total(self, years=None):
        query_params = {'pfi': self.id}
        if years:
            query_params.update({'annee__in': years})

        depense = Depense.objects.filter(**query_params)\
            .annotate(enveloppe=F('naturecomptabledepense__enveloppe'))\
            .values('annee', 'periodebudget__code', 'enveloppe')\
            .annotate(sum_depense_ae=Sum('montant_ae'),
                      sum_depense_cp=Sum('montant_cp'),
                      sum_depense_dc=Sum('montant_dc'))
        recette = Recette.objects.filter(**query_params)\
            .annotate(enveloppe=F('naturecomptablerecette__enveloppe'))\
            .values('annee', 'periodebudget__code', 'enveloppe')\
            .annotate(sum_recette_ar=Sum('montant_ar'),
                      sum_recette_re=Sum('montant_re'),
                      sum_recette_dc=Sum('montant_dc'))

        return depense, recette

    def get_years(self, begin_current_period=True, year_number=4):
        from .utils import get_current_year

        if self.date_debut and self.date_fin:
            begin_year = get_current_year() if begin_current_period\
                else self.date_debut.year
            end_year = min(begin_year + year_number, self.date_fin.year)
            return list(range(begin_year, end_year + 1))
        return []

    def get_total_types(self):
        # FIXME: docstring
        """
        Output format example for "depense":
        [
            {'AE': [
                {'Investissement': [
                    {2017: Decimal(1), 2018: Decimal(2)},
                    Decimal(3)],  # Total per "Investissement"
                'Personnel': [
                    {2017: Decimal(10), 2018: Decimal(20)},
                    Decimal(30)],  # Total per "Personnal"
                'Fonctionnement': [
                    {2017: Decimal(100), 2018: Decimal(200)},
                    Decimal(300)]  # Total per "Fonctionnement"
                },
                {2017: Decimal(111), 2018: Decimal(222)}],  # Totals per year
            'CP': [...]}
        ]
        """
        montants_dict = {'gbcp': ('AE', 'CP', 'AR', 'RE'), 'dc': ('DC',)}
        montant_type = lambda x: [
            k for k, v in montants_dict.items() if x in v][0]
        types = []
        years = self.get_years()

        for comptabilite in self.get_total(years=years):
            compta_types = {k: {} for k in montants_dict.keys()}
            for c in comptabilite:
                fields = [k for k in c.keys() if k.startswith('sum_')]
                for field in fields:
                    periode = c['periodebudget__code']
                    montant = c[field]
                    annee = c['annee']
                    field_name = field.split('_')[-1].upper()
                    mt = montant_type(field_name)
                    ct = compta_types[mt]
                    periode_dict = ct.setdefault(periode, {})
                    type_dict = periode_dict.setdefault(
                        field_name, [{}, dict.fromkeys(years, None)])
                    nature_dict = type_dict[0].setdefault(
                        c['enveloppe'], [dict.fromkeys(years, None), None])
                    nature_dict[0][annee] = montant
                    nature_dict[0][annee] = montant
                    # Total per enveloppe
                    nature_dict[1] = (nature_dict[1] or Decimal(0)) + montant

                    # Total per type
                    type_dict[1].setdefault(annee, None)
                    type_dict[1][annee] =\
                        (type_dict[1][annee] or Decimal(0)) + montant
                    type_dict[1]['total'] =\
                        type_dict[1].get('total', Decimal(0)) + montant
            types.append(compta_types)
        return types

    def get_detail_pfi_by_period(self, totals):
        # FIXME: docstring
        montants_dict = {'gbcp': ('AE', 'CP', 'AR', 'RE'), 'dc': ('DC',)}
        montant_type = lambda x: [
            k for k, v in montants_dict.items() if x in v][0]
        details = []

        # Group by year
        for compta in totals:
            compta_details = {}
            for year, year_values in groupby(compta, lambda x: x['annee']):
                compta_types = {k: [{}, {}] for k in montants_dict.keys()}
                periodes_set = set()
                for c in year_values:
                    periode = c['periodebudget__code']
                    periodes_set.add(periode)
                    fields = [k for k in c.keys() if k.startswith('sum_')]
                    for field in fields:
                        montant = c[field]
                        field_name = field.split('_')[-1].upper()
                        mt = montant_type(field_name)
                        ct = compta_types[mt]
                        nature_dict = ct[0].setdefault(
                            c['enveloppe'], [{}, {}])
                        type_dict = nature_dict[0].setdefault(
                            periode, {})
                        type_dict[field_name] = montant

                        # Total per periode and montant_type
                        nature_dict[1].setdefault(field_name, Decimal(0))
                        nature_dict[1][field_name] += montant

                        # Total per enveloppe
                        total_enveloppe = compta_types[mt][1].setdefault(periode, {})
                        total_enveloppe[field_name] = total_enveloppe.get(field_name, Decimal(0)) + montant

                # TODO: order periodes_set and global periodes_set for depenses and recettes
                compta_details[year] = (compta_types, periodes_set)
            details.append(compta_details)
        return details


class NatureComptableDepense(models.Model):

    enveloppe = models.CharField(max_length=100, verbose_name='Enveloppe')
    label_nature_comptable = models.CharField(
        max_length=255, verbose_name='Désignation de la nature comptable')
    code_nature_comptable = models.CharField(
        max_length=100, verbose_name='Code de la nature comptable')
    code_compte_budgetaire = models.CharField(
        max_length=100, verbose_name='Code du compte budgétaire')
    label_compte_budgetaire = models.CharField(
        max_length=255, verbose_name='Désignation du compte budgétaire')
    is_fleche = models.BooleanField('Fleché', max_length=100, default=True)
    is_decalage_tresorerie = models.BooleanField(
        max_length=100, verbose_name='Décalage trésorerie')
    is_non_budgetaire = models.BooleanField(
        max_length=100, verbose_name='Non budgétaire')
    is_pi_cfg = models.BooleanField(
        max_length=100, verbose_name='PI/CFG')
    is_active = models.BooleanField('Actif', max_length=100, default=True)
    priority = models.PositiveIntegerField('Ordre de tri pour les natures \
                                            comptables', default=1)
    ordre = models.PositiveIntegerField('Sous-ordre de tri pour les natures \
                                         comptables', default=1)

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return '{0.code_nature_comptable} - {0.label_nature_comptable}'\
            .format(self)


class NatureComptableRecette(models.Model):

    enveloppe = models.CharField(max_length=100, verbose_name='Enveloppe')
    code_fonds = models.CharField(max_length=100, verbose_name='Code du fonds')
    label_fonds = models.CharField(max_length=255,
                                   verbose_name='Désignation du fonds')
    code_nature_comptable = models.CharField(
        max_length=100, verbose_name='Code de la nature comptable')
    label_nature_comptable = models.CharField(
        max_length=255, verbose_name='Désignation de la nature comptable')
    code_compte_budgetaire = models.CharField(
        max_length=100, verbose_name='Code du compte budgétaire')
    label_compte_budgetaire = models.CharField(
        max_length=255, verbose_name='Désignation du compte budgétaire')
    is_fleche = models.BooleanField('Fleché', max_length=100, default=True)
    is_ar_and_re = models.BooleanField('AR et RE', max_length=100)
    is_non_budgetaire = models.BooleanField(
        'Non budgétaire dont PI', max_length=100)
    is_active = models.BooleanField('Actif', max_length=100, default=True)
    priority = models.PositiveIntegerField('Ordre de tri pour les natures \
                                            comptables', default=1)
    ordre = models.PositiveIntegerField('Sous-ordre de tri pour les natures \
                                         comptables', default=1)
    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return '{0.code_nature_comptable} - {0.label_nature_comptable}'\
            .format(self)


class StructureMontant(models.Model):
    structure = models.ForeignKey(Structure)
    periodebudget = models.ForeignKey('PeriodeBudget',
                                      related_name='periodebudgetmontants')
    depense_montant_dc = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal(0))
    depense_montant_cp = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal(0))
    depense_montant_ae = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal(0))
    recette_montant_dc = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal(0))
    recette_montant_re = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal(0))
    recette_montant_ar = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal(0))
    modification_date = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_period = ActivePeriodManager()

    class Meta:
        unique_together = (('structure', 'periodebudget'),)


class Comptabilite(models.Model):
    pfi = models.ForeignKey('PlanFinancement',
                            verbose_name='Plan de financement')
    structure = models.ForeignKey('Structure',
                                  verbose_name='Centre financier')
    commentaire = models.TextField(blank=True, null=True)
    lienpiecejointe = models.CharField(max_length=255,
                                       verbose_name='Lien vers un fichier',
                                       validators=[URLValidator()],
                                       blank=True, null=True)
    periodebudget = models.ForeignKey('PeriodeBudget',
                                      verbose_name='Période budgétaire')
    annee = models.PositiveIntegerField(verbose_name='Année')
    creele = models.DateTimeField(auto_now_add=True, blank=True)
    creepar = models.CharField(max_length=100, blank=True, null=True)
    modifiele = models.DateTimeField(verbose_name='Date de modification',
                                     auto_now=True, blank=True)
    modifiepar = models.CharField(max_length=100, blank=True, null=True)

    objects = models.Manager()
    active_period = ActivePeriodManager()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        self.initial_montants = kwargs.pop('initial_montants', ())
        super().__init__(*args, **kwargs)
        # Set the initial montants values for the difference calculation.
        # The values are set to 0 if it is a new object.
        list(map(lambda x: setattr(
                self, 'initial_%s' % x,
                getattr(self, x) if self.id else Decimal(0)),
            self.initial_montants))

    @transaction.atomic
    @require_lock(StructureMontant)
    def save(self, *args, **kwargs):
        """
        Change all the StructureMontant of the structure's asending hierarchy
        """
        comptabilite = kwargs.pop('comptabilite_type')

        super().save(*args, **kwargs)
        # Get the ascending hierarchy
        structures = [self.structure] + self.structure.get_ancestors()
        # Difference with the original values
        diffs = {m: getattr(self, m) - (
            getattr(self, 'initial_%s' % m) or Decimal(0))\
                for m in self.initial_montants}

        montant_name = lambda x: '%s_%s' % (comptabilite, x)
        for structure in structures:
            try:
                obj = StructureMontant.objects.get(
                    structure=structure, periodebudget=self.periodebudget
                )
                updated_values = {montant_name(k): (F(montant_name(k)) + v)\
                    for k, v in diffs.items()}
                for key, value in updated_values.items():
                    setattr(obj, key, value)
                obj.save()
            except StructureMontant.DoesNotExist:
                updated_values = {montant_name(k): v for k, v in diffs.items()}
                updated_values.update({
                    'structure': structure,
                    'periodebudget': self.periodebudget
                })
                obj = StructureMontant(**updated_values)
                obj.save()

    @transaction.atomic
    @require_lock(StructureMontant)
    def delete(self, **kwargs):
        """
        Change all the StructureMontant of the structure's asending hierarchy
        """
        comptabilite = kwargs.pop('comptabilite_type')
        montant_name = lambda x: '%s_%s' % (comptabilite, x)

        # Get the ascending hierarchy
        structures = [self.structure] + self.structure.get_ancestors()
        for structure in structures:
            montant = StructureMontant.objects.get(
                structure=structure, periodebudget=self.periodebudget)
            updated_values = {
                montant_name(m): getattr(montant, montant_name(m))\
                    - getattr(self, m) for m in self.initial_montants}
            for key, value in updated_values.items():
                setattr(montant, key, value)
            montant.save()
        super().delete(**kwargs)


class Depense(Comptabilite):
    montant_dc = models.DecimalField(verbose_name='Charges / Immo',
                                     max_digits=12, decimal_places=2,
                                     blank=True, null=True)
    montant_cp = models.DecimalField(verbose_name='Montant Crédit de Paiement',
                                     max_digits=12, decimal_places=2,
                                     blank=True, null=True)
    montant_ae = models.DecimalField(
        verbose_name='Montant Autorisation d\'Engagement',
        max_digits=12, decimal_places=2, blank=True, null=True)
    fonds = models.CharField(max_length=100, default='NA', editable=False)
    domainefonctionnel = models.ForeignKey('DomaineFonctionnel',
                                           verbose_name='Domaine fonctionnel')
    naturecomptabledepense = models.ForeignKey(
        'NatureComptableDepense', verbose_name='Nature Comptable')

    def __init__(self, *args, **kwargs):
        kwargs.update(
            {'initial_montants': ('montant_dc', 'montant_cp', 'montant_ae')})
        super().__init__(*args, **kwargs)

    def delete(self, **kwargs):
        kwargs.update({'comptabilite_type': 'depense'})
        super().delete(**kwargs)

    def save(self, *args, **kwargs):
        kwargs.update({'comptabilite_type': 'depense'})
        super().save(**kwargs)


class Recette(Comptabilite):
    montant_dc = models.DecimalField(verbose_name='Produits / Ressources',
                                     max_digits=12, decimal_places=2,
                                     blank=True, null=True)
    montant_re = models.DecimalField(
        verbose_name='Montant Recette Encaissable',
        max_digits=12, decimal_places=2, blank=True, null=True)
    montant_ar = models.DecimalField(
        verbose_name='Montant Autorisation de Recette', max_digits=12,
        decimal_places=2, blank=True, null=True)
    domainefonctionnel = models.CharField(max_length=100, default='NA',
                                          editable=False)
    naturecomptablerecette = models.ForeignKey(
        'NatureComptableRecette', verbose_name='Nature Comptable')

    def __init__(self, *args, **kwargs):
        kwargs.update(
            {'initial_montants': ('montant_dc', 'montant_re', 'montant_ar')})
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        kwargs.update({'comptabilite_type': 'recette'})
        super().save(*args, **kwargs)

    def delete(self, **kwargs):
        kwargs.update({'comptabilite_type': 'recette'})
        super().delete(**kwargs)
