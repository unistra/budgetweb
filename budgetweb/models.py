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


class CompteBudget(models.Model):
    """
    Gestion des Comptes budgétaires
    """
    code = models.CharField('Code', max_length=20)
    label = models.CharField('Libellé', max_length=150, blank=True, default="")
    description = models.CharField('Description', max_length=150, blank=True,
                                   default="")

    def __str__(self):
        return '{0.code} :: {0.label}'.format(self)


class FondBudgetaire(models.Model):
    code = models.CharField('Code du Fond budgetaire', max_length=100)
    label = models.CharField('Libellé', max_length=100, default="")
#    enveloppe = models.CharField('Enveloppe', max_length=50, blank=True,
#                                 default="")

    def __str__(self):
        return '{0.code} :: {0.label}'.format(self)


class ComptaNature(models.Model):
    code = models.CharField('Code de la nature comptable', max_length=100)
    label = models.CharField('Libellé', max_length=100, default="")
#    enveloppe = models.CharField('Enveloppe', max_length=50, blank=True,
#                                 default="")

    def __str__(self):
        return self.label


class NatureComptable(models.Model):
    """
    Gestion des natures comptables. En cours de précisions
    """
    enveloppe = models.CharField('Enveloppe', max_length=50, blank=True,
                                 default="")
    fondbudget_recette = models.ForeignKey('FondBudgetaire', default='',
        blank=True, null=True, verbose_name=u'Fond budgetaire')
    naturec_dep = models.ForeignKey('ComptaNature', default='', blank=True,
        null=True, verbose_name=u'Nature comptable')
    pfifleche = models.BooleanField('Utilisé avec un PFI fléché o/n:',
                                    default=False)
    ncsecondairecode = models.CharField('Code nature comptable secondaire',
                                        max_length=100, default="")
    ccbd = models.ForeignKey('CompteBudget', blank=True, default="",
                             verbose_name=u'Compte budgétaire')
    decalagetresocpae = models.BooleanField(
        'Décalage de Trésorerie CP<>AE o/n:', default=False)
    nctype = models.CharField('Nature utilisée en recette ou en dépenses',
                              max_length=100, default="")
#    ccnamesecond = models.CharField(
#        'Libellé court nature comptable secondaire', max_length=100,
#        default="")

    def __str__(self):
        return '{0.enveloppe} -- {1}'.format(
            self, self.naturec_dep.code if self.nctype == 'dep'\
                else self.fondbudget_recette.code)


class DomaineFonctionnel(models.Model):
    """
    Gestion des domaines fonctionnels. En cours de précisions
    """
    dfcode = models.CharField('Code', max_length=100, default="", unique=True)
    dflabel = models.CharField('Libellé', max_length=100, default="",
                               unique=True)
    dfgrpcumul = models.CharField('Groupe de cumul', max_length=100,
                                  default="", blank=True)
    dfgrpfonc = models.CharField('Groupe fonctionnel', max_length=100,
                                 default="", blank=True)
    dfrmq = models.CharField('Remarque', max_length=100, default="",
                             blank=True)
    dfdesc = models.CharField('Description', max_length=100, default="",
                              blank=True)

    def __str__(self):
        return '{0.dfcode} -- {0.dflabel}'.format(self)


class Structure(models.Model):
    """
    Gestion de la hiérarchie des Objets CF/CP/CC. En cours de précisions
    """
    myid = models.CharField('Code', max_length=100, default='', blank=True)
    type = models.CharField('Type', max_length=100)
    name = models.CharField('Libellé court', max_length=100)
    label = models.CharField('Libellé long', max_length=100)
    parentid = models.CharField('Code de la structure père', max_length=100)
    parent = models.ForeignKey('Structure', blank=True, null=True,
        related_name='fils',
        verbose_name=u'Lien direct vers la structure parent')
    ordre = models.CharField('Ordre', max_length=100)
    niv = models.CharField('Niveau', max_length=100)
    bloq = models.CharField('Bloqué', max_length=100)
    modifdate = models.CharField('Date de modification', max_length=100,
                                 default="")
    modifpar = models.CharField('Modifié par', max_length=100)
    dfmc = models.CharField('DFMC', max_length=100)
    fdr = models.CharField('FDR', max_length=100)
    ccassoc = models.CharField('CC associé', max_length=100, blank=True,
                               null=True, default="")
    cpassoc = models.CharField('CP associé', max_length=100, blank=True,
                               null=True, default="")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{0.name} -- {0.label}'.format(self)


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


class DepenseFull(models.Model):
    """
    Gestion des Depenses. En cours de précisions
    """
    myid = models.CharField(max_length=100, default='', blank=True)
    structlev3 = models.ForeignKey('Structure',
        related_name='depensestructlev3', verbose_name=u'Structure-CF')
    cptdeplev1 = models.ForeignKey('NatureComptable', blank=True, null=True,
        related_name='depenses', verbose_name=u'Nature comptable')
    domfonc = models.ForeignKey('DomaineFonctionnel', blank=True, null=True,
        verbose_name=u'Domaine fonctionnel')
    plfi = models.ForeignKey('PlanFinancement',
                             verbose_name=u'Programme de financement')
    montant = models.CharField(max_length=100, blank=True, null=True)
    montantdc = models.DecimalField(max_digits=12, decimal_places=2,
                        blank=True, null=True)
    montantcp = models.DecimalField(max_digits=12, decimal_places=2,
                        blank=True, null=True)
    montantae = models.DecimalField(max_digits=12, decimal_places=2,
                        blank=True, null=True)
    dateae = models.DateField(blank=True, null=True)
    commentaire = models.CharField(max_length=100, blank=True, null=True)
    myfile = models.TextField('Lien vers un fichier',
                              validators=[URLValidator()], blank=True)
    periodebudget = models.ForeignKey('PeriodeBudget', blank=True, null=True,
                                      related_name='periodebudget1')
    creele = models.DateTimeField(auto_now_add=True, blank=True)
    creepar = models.CharField(max_length=100, blank=True, null=True)
    modifiele = models.DateTimeField('Date de modification', auto_now=True,
                                     blank=True)
    modifiepar = models.CharField(max_length=100, blank=True, null=True)

    def clean(self):
        montantae = self.montantae
        montantcp = self.montantcp

        if self.structlev3:
            pass
        else:
            raise ValidationError(
                {'structlev3': u'Veuillez choisir la structure'})
        if not self.plfi:
            raise ValidationError({'plfi': u'Veuillez choisir le PFI'})
        if self.cptdeplev1:
            decalagetreso = self.cptdeplev1.decalagetresocpae
            if decalagetreso == False:
                if montantae != montantcp:
                    raise ValidationError({'montantae': u'Pas de décalage de trésorerie sur cette nature comptable.Veuillez vous assurrer que montantae=montantcp.'})
        else:
            raise ValidationError({'cptdeplev1': u'Veuillez saisir la nature comptable'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super(DepenseFull, self).save(*args, **kwargs)


class RecetteFull(models.Model):
    """
    Gestion des Recettes. En cours de précisions
    """
    myid = models.CharField(max_length=100, default='', blank=True)
    structlev3 = models.ForeignKey('Structure', related_name='recstructlev3',
                                   verbose_name=u'Structure-CF')
    cptdeplev1 = models.ForeignKey('NatureComptable', related_name='recettes',
                                   verbose_name=u'Nature comptable')
    domfonc = models.ForeignKey('DomaineFonctionnel',
                                verbose_name=u'Domaine fonctionnel')
    plfi = models.ForeignKey('PlanFinancement',
                              verbose_name=u'Programme de financement')
    montant = models.DecimalField(max_digits=12, decimal_places=2,
                       blank=True, null=True)
    montantar = models.DecimalField(max_digits=12, decimal_places=2,
                       blank=True, null=True)
    montantre = models.DecimalField(max_digits=12, decimal_places=2,
                       blank=True, null=True)
    montantdc = models.DecimalField(max_digits=12, decimal_places=2,
                       blank=True, null=True)
    commentaire = models.CharField(max_length=100, blank=True, null=True)
    myfile = models.TextField('Lien vers un fichier',
                              validators=[URLValidator()], blank=True)
    periodebudget = models.ForeignKey('PeriodeBudget', blank=True, null=True,
                                      related_name='periodebudget2')
    creele = models.DateTimeField(auto_now_add=True, blank=True)
    creepar = models.CharField(max_length=100, blank=True, null=True)
    modifiele = models.DateTimeField('Date de modification', auto_now=True,
                                     blank=True)
    modifiepar = models.CharField(max_length=100, blank=True, null=True)

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        self.full_clean()
        super(RecetteFull, self).save(*args, **kwargs)
