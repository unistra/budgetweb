from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Authorisation(models.Model):
    """
    Gestion des autorisations utilisateurs sur les CF
    Possibilités: * P* PAIE* ou un nom précis
    """
    username = models.CharField(max_length=100)
    myobject = models.CharField(max_length=100)


class PeriodeBudget(models.Model):
    """
    Gestion des périodes de budget. Une seule active
    avec bloqué=False. Les dépenses et les recettes
    sont saisies pour une période
    """
    name = models.CharField('Libellé court', max_length=20)
    label = models.CharField('Libellé long', max_length=100)
    annee = models.DateField('Année', null=True)
    bloque = models.BooleanField('Bloqué (False=Actif)', default=True)

    def __str__(self):
        return '{0.name} -- {0.label} -- {0.annee.year}'.format(self)


class DomaineFonctionnel(models.Model):
    """
    Gestion des domaines fonctionnels. En cours de précisions
    """
    code = models.CharField('Code', max_length=100, default="", unique=True)
    label = models.CharField('Libellé', max_length=100, default="",
                             unique=True)
    is_active = models.BooleanField('Actif', max_length=100, default=True)

    def __str__(self):
        return '{0.dfcode} -- {0.dflabel}'.format(self)


class Structure(models.Model):
    """
    Gestion de la hiérarchie des Objets CF. En cours de précisions
    """
    type = models.CharField('Type', max_length=100)
    code = models.CharField('Code', max_length=100, unique=True)
    label = models.CharField('Libellé', max_length=100)
    parent = models.ForeignKey('Structure', blank=True, null=True,
        related_name='fils',
        verbose_name=u'Lien direct vers la structure parent')
    is_active = models.BooleanField('Actif', max_length=100, default=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return '{0.code} -- {0.label}'.format(self)


#myid : code court pour l operation
#name : designation de l operation
class PlanFinancement(models.Model):
    """
    Gestion des Plans de financement. En cours de précisions
    """
    myid = models.CharField('Code court', max_length=100, default='',
                            blank=True)
    name = models.CharField('Libellé', max_length=100)
    eotp = models.CharField("Code court de l'eotp", max_length=100)
    creele = models.DateTimeField('Date de création', auto_now_add=True,
                                  blank=True)
    creepar = models.CharField('Créé par', max_length=100, blank=True,
                               null=True)
    modifiele = models.DateTimeField('Date de modification', auto_now=True,
                                     blank=True)
    modifiepar = models.CharField('Modification par', max_length=100,
                                  blank=True, null=True)
    societe = models.CharField('Société', max_length=100, default="")
    cfassoc = models.CharField('Centre financier associé', max_length=100,
                               default="")
    ccassoc = models.CharField('Centre de coût associé', max_length=100,
                               default="")
    cpassoc = models.CharField('Centre de profit associé', max_length=100,
                               default="")
    fleche = models.BooleanField('Fléché oui/non', default=False)
    pluriannuel = models.BooleanField('Pluriannuel oui/non', default=False)
    cfassoclink = models.ForeignKey('Structure', blank=True, null=True,
                                    verbose_name=u'Lien direct vers le CF')
    date_debut = models.DateTimeField(
        'Date de début', null=True, blank=True,
        help_text=u'Date de début du programme de financement')
    date_fin = models.DateTimeField(
        'Date de fin', null=True, blank=True,
        help_text=u'Date de fin du programme de financement')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return 'PFI : {0.myid} -- Eotp : {0.eotp}'.format(self)

class NatureComptableDepense(models.Model):

    enveloppe = models.CharField(max_length=100, verbose_name='Enveloppe')
    label_nature_comptable = models.CharField(max_length=100,
                                              verbose_name='Désignation de la nature comptable')
    code_nature_comptable = models.CharField(max_length=100,
                                             verbose_name='Code de la nature comptable')
    code_compte_budgetaire = models.CharField(max_length=100,
                                              verbose_name='Code du compte budgétaire')
    label_compte_budgetaire = models.CharField(max_length=100,
                                               verbose_name='Désignation du compte budgétaire')
    is_fleche = models.BooleanField('Fleché', max_length=100, default=True)
    is_decalage_tresorerie = models.BooleanField('Décalage trésorerie',
                                                 max_length=100)
    is_active = models.BooleanField('Actif', max_length=100, default=True)

class NatureComptableRecette(models.Model):

    enveloppe = models.CharField(max_length=100, verbose_name='Enveloppe')
    label_fonds = models.CharField(max_length=100,
                                              verbose_name='Désignation de la nature comptable')
    code_fonds = models.CharField(max_length=100,
                                             verbose_name='Code de la nature comptable')
    code_nature_comptable = models.CharField(max_length=100,
                                              verbose_name='Code du compte budgétaire')
    label_nature_comptable = models.CharField(max_length=100,
                                               verbose_name='Désignation du compte budgétaire')
    code_compte_budgetaire = models.CharField(max_length=100,
                                              verbose_name='Code du compte budgétaire')
    label_compte_budgetaire = models.CharField(max_length=100,
                                               verbose_name='Désignation du compte budgétaire')
    is_fleche = models.BooleanField('Fleché', max_length=100, default=True)
    is_active = models.BooleanField('Actif', max_length=100, default=True)

class Depense(models.Model):
    pfi = models.ForeignKey('PlanFinancement',
                            verbose_name='Programme de financement')
    strcture = models.ForeignKey('Structure',
                                 verbose_name='Centre financier')
    montantDC = models.DecimalField(max_digits=12, decimal_places=2,
                                    blank=True, null=True)
    montantCP = models.DecimalField(verbose_name='Montant Crédit de Paiement',
                                    max_digits=12, decimal_places=2,
                                    blank=True, null=True)
    montantAE = models.DecimalField(verbose_name='Montant Autorisation d\'Engagement',
                                    max_digits=12, decimal_places=2,
                                    blank=True, null=True)
    fonds = models.CharField(max_length=100, default='NA', editable=False)
    domainefonctionnel = models.ForeignKey('DomaineFonctionnel',
                                           verbose_name='Domaine fonctionnel')
    naturecomptabledepense = models.ForeignKey('NatureComptableDepense',
                                               verbose_name='Nature Comptable Dépense')
    commentaire = models.TextField(blank=True, null=True)
    lienpiecejointe = models.CharField(max_length=255,
                                       verbose_name='Lien vers un fichier',
                                       validators=[URLValidator()],
                                       blank=True)
    periodebudget = models.ForeignKey('PeriodeBudget', blank=True, null=True,
                                       related_name='periodebudgetdepense')
    annee = models.PositiveIntegerField(verbose_name='Année de la saisie')
    creele = models.DateTimeField(auto_now_add=True, blank=True)
    creepar = models.CharField(max_length=100, blank=True, null=True)
    modifiele = models.DateTimeField(verbose_name='Date de modification', auto_now=True,
                                     blank=True)
    modifiepar = models.CharField(max_length=100, blank=True, null=True)

    #def clean(self):
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
    #                raise ValidationError({'montantae': u'Pas de décalage de trésorerie sur cette nature comptable.Veuillez vous assurrer que montantae=montantcp.'})
    #    else:
    #        raise ValidationError({'cptdeplev1': u'Veuillez saisir la nature comptable'})
    #
    #def save(self, *args, **kwargs):
    #    self.full_clean()
    #    super(DepenseFull, self).save(*args, **kwargs)

class Recette(models.Model):
    pfi = models.ForeignKey('PlanFinancement',
                            verbose_name='Programme de financement')
    strcture = models.ForeignKey('Structure',
                                 verbose_name='Centre financier')
    montantDC = models.DecimalField(max_digits=12, decimal_places=2,
                                    blank=True, null=True)
    montantRE = models.DecimalField(verbose_name='Montant Recette Encaissable',
                                    max_digits=12, decimal_places=2,
                                    blank=True, null=True)
    montantAR = models.DecimalField(verbose_name='Montant Autorisation de Recette',
                                    max_digits=12, decimal_places=2,
                                    blank=True, null=True)
    domainefonctionnel = models.CharField(max_length=100, default='NA', editable=False)
    naturecomptablerecette = models.ForeignKey('NatureComptableRecette',
                                               verbose_name='Nature Comptable Recette')
    commentaire = models.TextField(blank=True, null=True)
    lienpiecejointe = models.CharField(max_length=255,
                                       verbose_name='Lien vers un fichier',
                                       validators=[URLValidator()],
                                       blank=True)
    periodebudget = models.ForeignKey('PeriodeBudget', blank=True, null=True,
                                       related_name='periodebudgetrecette')
    annee = models.PositiveIntegerField(verbose_name='Année de la saisie')
    creele = models.DateTimeField(auto_now_add=True, blank=True)
    creepar = models.CharField(max_length=100, blank=True, null=True)
    modifiele = models.DateTimeField(verbose_name='Date de modification', auto_now=True,
                                     blank=True)
    modifiepar = models.CharField(max_length=100, blank=True, null=True)

    #def clean(self):
    #    pass
    #
    #def save(self, *args, **kwargs):
    #    self.full_clean()
    #    super(RecetteFull, self).save(*args, **kwargs)
