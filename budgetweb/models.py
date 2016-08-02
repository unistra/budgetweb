from decimal import Decimal

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models, transaction
from django.db.models import F, Sum
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
        return '{0.label_court}'.format(self)


class Structure(models.Model):
    """
    Gestion de la hiérarchie des Objets CF. En cours de précisions
    """
    type = models.CharField('Type', max_length=100)
    code = models.CharField('Code', max_length=100, unique=True)
    label = models.CharField('Libellé', max_length=255)
    parent = models.ForeignKey(
        'Structure', blank=True, null=True, related_name='fils',
        verbose_name=u'Lien direct vers la structure parent')
    is_active = models.BooleanField('Actif', max_length=100, default=True)
    # Depth: 1 == root
    depth = models.PositiveIntegerField()
    # Path: id_root/id_ancestor1/id_ancestor2/...
    path = models.TextField(_('Path'), blank=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ['code']

    def __str__(self):
        return '{0.code}'.format(self)

    def save(self, *args, **kwargs):
        parent = self.parent
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

    def get_sons(self):
        return self.fils.filter(is_active=True).order_by('code')

    def get_subtree(self):
        return ({son: son.get_subtree()} for son in self.get_sons())

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
    def getTotal(self):
        # select annee, periodebudget_id, enveloppe, sum(montantae) as sommeae,
        # sum(montantcp) as sommecp, sum(montantdc) as sommedc
        # from budgetweb_depense, budgetweb_naturecomptabledepense
        # where budgetweb_naturecomptabledepense.id = \
        #       budgetweb_depense.naturecomptabledepense_id
        # and pfi_id=30 group by annee, periodebudget_id, enveloppe;
        depense = Depense.objects.filter(pfi=self.id) \
               .values('annee', 'periodebudget',
                       'naturecomptabledepense__enveloppe') \
               .annotate(sommeDepenseAE=Sum('montant_ae'),
                         sommeDepenseCP=Sum('montant_cp'),
                         sommeDepenseDC=Sum('montant_dc'))
        recette = Recette.objects.filter(pfi=self.id) \
               .values('annee', 'periodebudget',
                       'naturecomptablerecette__enveloppe') \
               .annotate(sommeRecetteAE=Sum('montant_ar'),
                         sommeRecetteCP=Sum('montant_re'),
                         sommeRecetteDC=Sum('montant_dc'))

        return depense, recette


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
    is_active = models.BooleanField('Actif', max_length=100, default=True)

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return '{0.code_nature_comptable} - \
                {0.label_nature_comptable}'.format(self)


class NatureComptableRecette(models.Model):

    enveloppe = models.CharField(max_length=100, verbose_name='Enveloppe')
    label_fonds = models.CharField(
        max_length=255,
        verbose_name='Désignation de la nature comptable')
    code_fonds = models.CharField(max_length=100, verbose_name='Code du fond')
    code_nature_comptable = models.CharField(
        max_length=100, verbose_name='Code de la nature comptable')
    label_nature_comptable = models.CharField(
        max_length=255, verbose_name='Désignation du compte budgétaire')
    code_compte_budgetaire = models.CharField(
        max_length=100, verbose_name='Code du compte budgétaire')
    label_compte_budgetaire = models.CharField(
        max_length=255, verbose_name='Désignation du compte budgétaire')
    is_fleche = models.BooleanField('Fleché', max_length=100, default=True)
    is_active = models.BooleanField('Actif', max_length=100, default=True)

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return '{0.code_nature_comptable} - \
                {0.label_nature_comptable}'.format(self)


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
        list(map(lambda x: setattr(self, 'initial_%s' % x, getattr(self, x)),
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


class Depense(Comptabilite):
    montant_dc = models.DecimalField(max_digits=12, decimal_places=2,
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

    def save(self, *args, **kwargs):
        kwargs.update({'comptabilite_type': 'depense'})
        super().save(*args, **kwargs)

    def delete(self, **kwargs):
        kwargs.update({'comptabilite_type': 'depense'})
        super().delete(**kwargs)

    # def clean(self):
    #    montantae = self.montantae
    #    montantcp = self.montantcp
    #
    #    if self.structlev3:
    #        pass
    #    else:
    #        raise ValidationError(
    #            {'structlev3': u'Veuillez choisir la structure'})
    #    if not self.plfi:
    #        raise ValidationError({'plfi': u'Veuillez choisir le PFI'})
    #    if self.cptdeplev1:
    #        decalagetreso = self.cptdeplev1.decalagetresocpae
    #        if decalagetreso == False:
    #            if montantae != montantcp:
    #                raise ValidationError({'montantae': u'Pas de décalage de
    # trésorerie sur cette nature comptable.Veuillez vous assurrer que
    # montantae=montantcp.'})
    #    else:
    #        raise ValidationError({'cptdeplev1':
    #        u'Veuillez saisir la nature comptable'})
    #
    # def save(self, *args, **kwargs):
    #    self.full_clean()
    #    super(DepenseFull, self).save(*args, **kwargs)


class Recette(Comptabilite):
    montant_dc = models.DecimalField(max_digits=12, decimal_places=2,
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
