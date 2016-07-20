from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset()\
            .filter(is_active=True)


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

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ['code']

    def __str__(self):
        return '{0.code}'.format(self)

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


class Depense(models.Model):
    pfi = models.ForeignKey('PlanFinancement',
                            verbose_name='Programme de financement')
    structure = models.ForeignKey('Structure',
                                  verbose_name='Centre financier')
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
    commentaire = models.TextField(blank=True, null=True)
    lienpiecejointe = models.CharField(max_length=255,
                                       verbose_name='Lien vers un fichier',
                                       validators=[URLValidator()],
                                       blank=True, null=True)
    periodebudget = models.ForeignKey('PeriodeBudget',
                                      verbose_name='Période budgétaire',
                                      related_name='periodebudgetdepense')
    annee = models.PositiveIntegerField(verbose_name='Année')
    creele = models.DateTimeField(auto_now_add=True, blank=True)
    creepar = models.CharField(max_length=100, blank=True, null=True)
    modifiele = models.DateTimeField(verbose_name='Date de modification',
                                     auto_now=True, blank=True)
    modifiepar = models.CharField(max_length=100, blank=True, null=True)

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


class Recette(models.Model):
    pfi = models.ForeignKey('PlanFinancement',
                            verbose_name='Programme de financement')
    structure = models.ForeignKey('Structure',
                                  verbose_name='Centre financier')
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
    commentaire = models.TextField(blank=True, null=True)
    lienpiecejointe = models.CharField(max_length=255,
                                       verbose_name='Lien vers un fichier',
                                       validators=[URLValidator()],
                                       blank=True, null=True)
    periodebudget = models.ForeignKey('PeriodeBudget',
                                      verbose_name='Période budgétaire',
                                      related_name='periodebudgetrecette')
    annee = models.PositiveIntegerField(verbose_name='Année')
    creele = models.DateTimeField(auto_now_add=True, blank=True)
    creepar = models.CharField(max_length=100, blank=True, null=True)
    modifiele = models.DateTimeField(verbose_name='Date de modification',
                                     auto_now=True, blank=True)
    modifiepar = models.CharField(max_length=100, blank=True, null=True)
