from decimal import Decimal

from django.conf import settings
from django.core.validators import URLValidator
from django.db import models, transaction
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from budgetweb.apps.structure.models import Structure
from .decorators import require_lock


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class ActiveVirementManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True,
                                             period__code__startswith='VIR')


class ActiveBudgetManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True,
                                             period__code__startswith='B')


class ActivePeriodManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().\
            filter(periodebudget__is_active=True).\
            filter(periodebudget__period__code__startswith='B')


class StructureAuthorizations(models.Model):
    """
    Gestion des autorisations utilisateurs sur les CF
    Possibilités: * P* PAIE* ou un nom précis
    """
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL)
    structures = models.ManyToManyField('structure.Structure',
                                        related_name='authorized_structures')

    class Meta:
        verbose_name = _('structure authorizations')
        verbose_name_plural = _('structures authorizations')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.pk:
            for structure in self.structures.all():
                for children in structure.get_children():
                    self.structures.add(children)
        super().save(*args, **kwargs)


@receiver(post_save, sender=Structure)
def my_handler(sender, instance, created, **kwargs):
        parent = instance.parent
        # Add the parent's authorizations for a newly created structure
        if parent and created:
            for auth in parent.authorized_structures.all():
                auth.structures.add(instance)


class Period(models.Model):

    code = models.CharField(_('Code'), max_length=20)
    label = models.CharField(_('Label'), max_length=255)
    order = models.PositiveIntegerField(_('Order'), default=0)

    def __str__(self):
        return '{0.code} - {0.label}'.format(self)


class PeriodeBudget(models.Model):
    """
    Gestion des périodes de budget. Une seule active
    avec bloqué=False. Les dépenses et les recettes
    sont saisies pour une période
    """

    period = models.ForeignKey(Period, verbose_name=_('Period'))
    annee = models.PositiveIntegerField('Année')
    is_active = models.BooleanField('Activé (oui/non)', default=True)

    # Différentes dates pour les saisies.
    date_debut_saisie = models.DateField('Date de début de la saisie \
                                          pour les utilisateurs',
                                         blank=True, null=True)
    date_fin_saisie = \
        models.DateField('Date de fin de la saisie pour les utilisateurs',
                         blank=True, null=True)
    date_debut_retardataire = \
        models.DateField('Date de début de la saisie pour les utilisateurs \
                          appartenant au groupe RETARDATAIRE',
                         blank=True, null=True)
    date_fin_retardataire = \
        models.DateField('Date de fin de la saisie pour les utilisateurs \
                          appartenant au groupe RETARDATAIRE',
                         blank=True, null=True)
    date_debut_dfi = \
        models.DateField('Date de début de la saisie pour les utilisateurs \
                          appartenant au groupe DFI', blank=True, null=True)
    date_fin_dfi = \
        models.DateField('Date de fin de la saisie pour les utilisateurs \
                          appartenant au groupe DFI', blank=True, null=True)
    date_debut_admin = \
        models.DateField('Date de début de la saisie pour les \
                          super-utilisateurs', blank=True, null=True)
    date_fin_admin = \
        models.DateField('Date de fin de la saisie pour les \
                          superutilisateurs', blank=True, null=True)

    objects = models.Manager()
    # Un premier manager pour récupérer les periodes actives
    active = ActiveManager()
    # Un deuxième manager pour récupérer la période Virement active (VIRx)
    activevirement = ActiveVirementManager()
    # Un troisième manager pour récupérer la période Budgétaire active (BI/BRx)
    activebudget = ActiveBudgetManager()

    class Meta:
        verbose_name = _('budget period')
        verbose_name_plural = _('budget periods')

    def __str__(self):
        return '{0.period} - {0.annee}'.format(self)

    def has_entries(self):
        return self.depense_set.exists() or self.recette_set.exists()


class StructureMontant(models.Model):
    structure = models.ForeignKey('structure.Structure')
    periodebudget = models.ForeignKey('PeriodeBudget',
                                      related_name='periodebudgetmontants')
    annee = models.PositiveIntegerField(verbose_name='Année')
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
        unique_together = (('structure', 'periodebudget', 'annee'),)
        verbose_name = _('structure amounts')
        verbose_name_plural = _('structures amounts')


class Comptabilite(models.Model):
    pfi = models.ForeignKey('structure.PlanFinancement',
                            verbose_name='Plan de financement')
    structure = models.ForeignKey('structure.Structure',
                                  verbose_name='Centre financier')
    commentaire = models.TextField(blank=True, null=True)
    lienpiecejointe = models.CharField(max_length=255,
                                       verbose_name='Lien vers un fichier',
                                       validators=[URLValidator()],
                                       blank=True, null=True)
    periodebudget = models.ForeignKey('PeriodeBudget',
                                      verbose_name='Période budgétaire')
    annee = models.PositiveIntegerField(verbose_name='Année')
    virement = models.ForeignKey(
        'Virement',
        verbose_name="Renvoie vers le virement correspondant s'il existe",
        null=True, blank=True)
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
                getattr(self, x, Decimal(0))),
            self.initial_montants))

    @transaction.atomic
    @require_lock([StructureMontant, 'budgetweb.Depense', 'budgetweb.Recette'])
    def save(self, *args, **kwargs):
        """
        Change all the StructureMontant of the structure's ascending hierarchy
        """
        comptabilite = self.__class__.__name__.lower()
        initial = None
        if self.pk:
            initial = self.__class__.objects.get(pk=self.pk)

        super().save(*args, **kwargs)
        # Get the ascending hierarchy
        structures = [self.structure] + self.structure.get_ancestors()
        # Difference with the original values
        diffs = {m: getattr(self, m) - (
            getattr(initial, m, None) or Decimal(0))\
                for m in self.initial_montants}

        montant_name = lambda x: '%s_%s' % (comptabilite, x)
        for structure in structures:
            try:
                obj = StructureMontant.objects.get(
                    structure=structure.pk,
                    periodebudget=self.periodebudget.pk, annee=self.annee
                )

                updated_values = {montant_name(k): (F(montant_name(k)) + v)\
                    for k, v in diffs.items()}
                for key, value in updated_values.items():
                    setattr(obj, key, value)
                obj.save(update_fields=updated_values.keys())
            except StructureMontant.DoesNotExist:
                updated_values = {montant_name(k): v for k, v in diffs.items()}
                updated_values.update({
                    'structure': structure,
                    'periodebudget': self.periodebudget,
                    'annee': self.annee
                })
                obj = StructureMontant(**updated_values)
                obj.save()

    @transaction.atomic
    @require_lock([StructureMontant, 'budgetweb.Depense', 'budgetweb.Recette'])
    def delete(self, **kwargs):
        """
        Change all the StructureMontant of the structure's asending hierarchy
        """
        comptabilite = self.__class__.__name__.lower()
        montant_name = lambda x: '%s_%s' % (comptabilite, x)

        # Get the ascending hierarchy
        structures = [self.structure] + self.structure.get_ancestors()
        for structure in structures:
            montant = StructureMontant.objects.get(
                structure=structure, periodebudget=self.periodebudget,
                annee=self.annee)
            updated_values = {
                montant_name(m): getattr(montant, montant_name(m))
                - getattr(self, 'initial_%s' % m) for m in self.initial_montants}
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
    domainefonctionnel = models.ForeignKey('structure.DomaineFonctionnel',
                                           verbose_name='Domaine fonctionnel')
    naturecomptabledepense = models.ForeignKey(
        'structure.NatureComptableDepense', verbose_name='Nature Comptable')

    class Meta:
        verbose_name = _('expense')
        verbose_name_plural = _('expenses')

    def __init__(self, *args, **kwargs):
        kwargs.update(
            {'initial_montants': ('montant_dc', 'montant_cp', 'montant_ae')})
        super().__init__(*args, **kwargs)


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
        'structure.NatureComptableRecette', verbose_name='Nature Comptable')

    class Meta:
        verbose_name = _('receipt')
        verbose_name_plural = _('receipts')

    def __init__(self, *args, **kwargs):
        kwargs.update(
            {'initial_montants': ('montant_dc', 'montant_re', 'montant_ar')})
        super().__init__(*args, **kwargs)


class Virement(models.Model):
    document_number = models.PositiveIntegerField(
                        verbose_name='Numéro de document SIFAC')
    document_type = models.CharField(
                        verbose_name="Type de document SIFAC",
                        max_length=100)
    version = models.CharField(
                        verbose_name="Version de budget",
                        max_length=100)
    perimetre = models.CharField(verbose_name="Périmètre financier",
                                 max_length=10)
    process = models.CharField(verbose_name="Type de virement", max_length=10)
    creator_login = models.CharField(
                        verbose_name="Compte SIFAC ayant créé le virement",
                        max_length=100)
    creation_date = models.DateTimeField(
                        verbose_name="Date de création du virement")
    value_date = models.DateField(verbose_name="Date de valeur")

    class Meta:
        verbose_name = _('transfer')
        verbose_name_plural = _('transfers')
