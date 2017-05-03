from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class DomaineFonctionnel(models.Model):
    """
    Gestion des domaines fonctionnels. En cours de précisions
    """
    code = models.CharField(_('Code'), max_length=100, default="", unique=True)
    label = models.CharField(_('Label'), max_length=255, default="")
    label_court = models.CharField(_('Short label'), max_length=100, default="",
                                   null=True, blank=True,)
    is_active = models.BooleanField(_('Is active'), max_length=100, default=True)

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return '{0.code} - {0.label_court}'.format(self)


class Structure(models.Model):
    """
    Gestion de la hiérarchie des Objets CF. En cours de précisions
    """
    code = models.CharField(_('Code'), max_length=100, unique=True)
    label = models.CharField(_('Label'), max_length=255)
    parent = models.ForeignKey(
        'Structure', blank=True, null=True, related_name='fils',
        verbose_name=u'Lien direct vers la structure parent')
    groupe1 = models.CharField(_('BudgetWeb group 1'), max_length=255,
                               blank=True, null=True)
    groupe2 = models.CharField(_('BudgetWeb group 2'), max_length=255,
                               blank=True, null=True)
    is_active = models.BooleanField(_('Is active'), max_length=100, default=True)
    # Depth: 1 == root
    depth = models.PositiveIntegerField(_('Depth'))
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

    def get_first_ancestor(self):
        if self.parent is None:
            return self
        else:
            return self.parent.get_first_ancestor()

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
                                  verbose_name=_('Structure'))
    code = models.CharField(_('Code'), max_length=100, default='NA')
    label = models.CharField(_('Label'), max_length=255)
    eotp = models.CharField(_('EOTP short label'), max_length=100)
    centrecoutderive = models.CharField(_('Related cost center'),
                                        max_length=100)
    centreprofitderive = models.CharField('Related profit center',
                                          max_length=100)
    groupe1 = models.CharField(_('BudgetWeb group 1'), max_length=255,
                               null=True, blank=True)
    groupe2 = models.CharField(_('BudgetWeb group 2'), max_length=255,
                               null=True, blank=True)
    is_fleche = models.BooleanField(_('Is labeled'), default=False)
    is_pluriannuel = models.BooleanField(_('Is multi-year'), default=False)
    is_active = models.BooleanField(_('Is active'), max_length=100, default=True)
    date_debut = models.DateField(_('Begin date'), null=True, blank=True,
                                  help_text='Date de début')
    date_fin = models.DateField(_('End date'), null=True, blank=True,
                                help_text='Date de fin')

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ['label']

    def __str__(self):
        return '{0.code}'.format(self)

    # # Retourne un tableau avec l'année
    # def get_total(self, years=None):
    #     query_params = {'pfi': self.id}
    #     if years:
    #         query_params.update({'annee__in': years})

    #     depense = Depense.objects.filter(**query_params)\
    #         .annotate(enveloppe=F('naturecomptabledepense__enveloppe'))\
    #         .values('annee', 'periodebudget__code', 'enveloppe')\
    #         .annotate(sum_depense_ae=Sum('montant_ae'),
    #                   sum_depense_cp=Sum('montant_cp'),
    #                   sum_depense_dc=Sum('montant_dc'))
    #     recette = Recette.objects.filter(**query_params)\
    #         .annotate(enveloppe=F('naturecomptablerecette__enveloppe'))\
    #         .values('annee', 'periodebudget__code', 'enveloppe')\
    #         .annotate(sum_recette_ar=Sum('montant_ar'),
    #                   sum_recette_re=Sum('montant_re'),
    #                   sum_recette_dc=Sum('montant_dc'))

    #     return depense, recette

    # def get_years(self, begin_current_period=False, year_number=4):
    #     from .utils import get_current_year

    #     if self.date_debut and self.date_fin:
    #         if begin_current_period:
    #             begin_year = self.date_debut.year
    #         else:
    #             begin_year = get_current_year()-1 if self.date_debut.year < get_current_year() else get_current_year()
    #         end_year = min(begin_year + year_number, self.date_fin.year)\
    #             if year_number else self.date_fin.year
    #         return list(range(begin_year, end_year + 1))
    #     return []

    # def get_total_types(self):
    #     # FIXME: docstring
    #     """
    #     Output format example for "depense":
    #     [
    #         {'AE': [
    #             {'Investissement': [
    #                 {2017: Decimal(1), 2018: Decimal(2)},
    #                 Decimal(3)],  # Total per "Investissement"
    #             'Personnel': [
    #                 {2017: Decimal(10), 2018: Decimal(20)},
    #                 Decimal(30)],  # Total per "Personnal"
    #             'Fonctionnement': [
    #                 {2017: Decimal(100), 2018: Decimal(200)},
    #                 Decimal(300)]  # Total per "Fonctionnement"
    #             },
    #             {2017: Decimal(111), 2018: Decimal(222)}],  # Totals per year
    #         'CP': [...]}
    #     ]
    #     """
    #     montants_dict = {'gbcp': ('AE', 'CP', 'AR', 'RE'), 'dc': ('DC',)}
    #     default_period = 'BI'
    #     montant_type = lambda x: [
    #         k for k, v in montants_dict.items() if x in v][0]
    #     types = []
    #     years = self.get_years()

    #     for comptabilite in self.get_total(years=years):
    #         compta_types = {k: {default_period: {}} for k in montants_dict.keys()}
    #         for c in comptabilite:
    #             fields = [k for k in c.keys() if k.startswith('sum_')]
    #             for field in fields:
    #                 periode = c['periodebudget__code']
    #                 montant = c[field]
    #                 annee = c['annee']
    #                 field_name = field.split('_')[-1].upper()
    #                 mt = montant_type(field_name)
    #                 ct = compta_types[mt]
    #                 periode_dict = ct.setdefault(periode, {})
    #                 type_dict = periode_dict.setdefault(
    #                     field_name, [{}, dict.fromkeys(years, None)])
    #                 nature_dict = type_dict[0].setdefault(
    #                     c['enveloppe'], [dict.fromkeys(years, None), None])
    #                 nature_dict[0][annee] = montant
    #                 nature_dict[0][annee] = montant
    #                 # Total per enveloppe
    #                 nature_dict[1] = (nature_dict[1] or Decimal(0)) + montant

    #                 # Total per type
    #                 type_dict[1].setdefault(annee, None)
    #                 type_dict[1][annee] =\
    #                     (type_dict[1][annee] or Decimal(0)) + montant
    #                 type_dict[1]['total'] =\
    #                     type_dict[1].get('total', Decimal(0)) + montant
    #         types.append(compta_types)
    #     return types


class NatureComptableDepense(models.Model):

    enveloppe = models.CharField(_('Envelope'), max_length=100)
    label_nature_comptable = models.CharField(_('Label'), max_length=255)
    code_nature_comptable = models.CharField(_('Code'), max_length=100)
    code_compte_budgetaire = models.CharField(
        _('Budget account code'), max_length=100)
    label_compte_budgetaire = models.CharField(
        _('Budget account label'), max_length=255)
    is_fleche = models.BooleanField(
        _('Is labeled'), max_length=100, default=True)
    is_decalage_tresorerie = models.BooleanField(
        _('Is cash shift'), max_length=100)
    is_non_budgetaire = models.BooleanField(
        _('Is non budgetary'), max_length=100)
    is_pi_cfg = models.BooleanField(_('Is PFI/CFG'), max_length=100)
    is_active = models.BooleanField(
        _('Is active'), max_length=100, default=True)
    priority = models.PositiveIntegerField(
        _('Sorting order for the accounting natures'), default=1)
    ordre = models.PositiveIntegerField(
        _('Sorting sub-order for the accounting natures'), default=1)

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return '{0.code_nature_comptable} - {0.label_nature_comptable}'\
            .format(self)


class NatureComptableRecette(models.Model):

    enveloppe = models.CharField(_('Envelope'), max_length=100)
    code_fonds = models.CharField(_('Funds code'), max_length=100)
    label_fonds = models.CharField(_('Funds label'), max_length=255)
    code_nature_comptable = models.CharField(_('Code'), max_length=100)
    label_nature_comptable = models.CharField(_('Label'), max_length=255)
    code_compte_budgetaire = models.CharField(
        _('Budget account code'), max_length=100)
    label_compte_budgetaire = models.CharField(
        _('Budget account label'), max_length=255)
    is_fleche = models.BooleanField(
        _('Is labeled'), max_length=100, default=True)
    is_ar_and_re = models.BooleanField(_('Is AR et RE'), max_length=100)
    is_non_budgetaire = models.BooleanField(
        _('Is non budgetary'), max_length=100)
    is_active = models.BooleanField(_(
        'Is active'), max_length=100, default=True)
    priority = models.PositiveIntegerField(
        _('Sorting order for the accounting natures'), default=1)
    ordre = models.PositiveIntegerField(
        _('Sorting sub-order for the accounting natures'), default=1)

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return '{0.code_nature_comptable} - {0.label_nature_comptable}'\
            .format(self)
