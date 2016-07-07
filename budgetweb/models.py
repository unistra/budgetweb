from __future__ import unicode_literals

from django.db import models
from django import forms

from django.utils import timezone
import operator
from django.core.validators import URLValidator

from django.db.models import Q
from datetime import datetime
from django.core.exceptions import ValidationError


"""----------------------------------------------
Gestion des autorisations utilisateurs sur les CF
Possibilités: * P* PAIE* ou un nom précis
----------------------------------------------"""
class Authorisation(models.Model):
    username = models.CharField(max_length=100)
    myobject = models.CharField(max_length=100)

"""----------------------------------------------
Gestion des périodes de budget. Une seule active
avec bloqué=False. Les dépenses et les recettes
sont saisies pour une période
----------------------------------------------"""
class PeriodeBudget(models.Model):
    name = models.CharField(max_length=20,verbose_name=u'Libellé court')
    label = models.CharField(max_length=100,verbose_name=u'Libellé long')
    annee = models.DateField( null=True,verbose_name=u'Année')
    bloque = models.BooleanField(default = True,
                   verbose_name=u'Bloqué (False=Actif)')

    def __str__(self):
        return (self.name + " -- " + self.label + " -- " + str(self.annee.year))


"""----------------------------------------------
Gestion des Comptes budgétaires 
----------------------------------------------"""
class CompteBudget(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'Code')
    label = models.CharField(max_length=150,blank=True,default="",verbose_name=u'Libellé')
    description = models.CharField(max_length=150,blank=True,default="",verbose_name=u'Description')

    def __str__(self):
        return (self.code +'::'+self.label)


class FondBudgetaire(models.Model):
    code = models.CharField(max_length=100,
            verbose_name=u'Code du Fond budgetaire')
    label = models.CharField(max_length=100,
            verbose_name=u'Libellé',default="")
#    enveloppe = models.CharField(max_length=50,blank=True,default="",verbose_name=u'Enveloppe')

    def __str__(self):
        return (self.code +'::'+self.label)


class ComptaNature(models.Model):
    code = models.CharField(max_length=100,
            verbose_name=u'Code de la nature comptable')
    label = models.CharField(max_length=100,
            verbose_name=u'Libellé',default="")
#    enveloppe = models.CharField(max_length=50,blank=True,default="",verbose_name=u'Enveloppe')

    def __str__(self):
        return (self.label)

"""----------------------------------------------
Gestion des natures comptables. En cours de précisions
----------------------------------------------"""
class NatureComptable(models.Model):
    enveloppe = models.CharField(max_length=50,blank=True,default="",verbose_name=u'Enveloppe')
    fondbudget_recette = models.ForeignKey('FondBudgetaire', default='',blank = True,null=True,verbose_name=u'Fond budgetaire')
    naturec_dep = models.ForeignKey('ComptaNature', default='',blank = True,null=True, verbose_name=u'Nature comptable')
    pfifleche = models.BooleanField(default=False,
            verbose_name=u'Utilisé avec un PFI fléché o/n:')
    ncsecondairecode = models.CharField(max_length=100,
         verbose_name=u'Code nature comptable secondaire',default="")
    ccbd = models.ForeignKey('CompteBudget', blank = True, default="",verbose_name=u'Compte budgétaire')
    decalagetresocpae = models.BooleanField(default=False,
            verbose_name=u'Décalage de Trésorerie CP<>AE o/n:')
    nctype = models.CharField(max_length=100,
            verbose_name=u'Nature utilisée en recette ou en dépenses',default="")
#    ccnamesecond = models.CharField(max_length=100,
#         verbose_name=u'Libellé court nature comptable secondaire',default="")

    def __str__(self):
        if self.nctype == 'dep':
            return (self.enveloppe +" -- "+ self.naturec_dep.code)
        else:
            return (self.enveloppe +" -- "+ self.fondbudget_recette.code)



"""----------------------------------------------
Gestion des domaines fonctionnels. En cours de précisions
----------------------------------------------"""
class DomaineFonctionnel(models.Model):
    dfcode = models.CharField(max_length=100, default="", verbose_name=u'Code',unique=True)
    dflabel = models.CharField(max_length=100, default="",
                verbose_name=u'Libellé',unique=True)
    dfgrpcumul = models.CharField(max_length=100, default="",
                verbose_name=u'Groupe de cumul',blank=True)
    dfgrpfonc = models.CharField(max_length=100, default="",
                verbose_name=u'Groupe fonctionnel',blank=True)
    dfrmq = models.CharField(max_length=100, default="",
                verbose_name='Remarque',blank=True)
    dfdesc = models.CharField(max_length=100, default="",
                verbose_name='Description',blank=True)

    def __str__(self):
        return (self.dfcode + " -- " + self.dflabel)



"""--------------------------------------------------------------
Gestion de la hiérarchie des Objets CF/CP/CC. En cours de précisions
----------------------------------------------------------------"""
class Structure(models.Model):
    myid = models.CharField(max_length=100, default='',blank=True,verbose_name=u'Code')
    type = models.CharField(max_length=100,verbose_name=u'Type')
    name = models.CharField(max_length=100,verbose_name=u'Libellé court')
    label = models.CharField(max_length=100,verbose_name=u'Libellé long')
    parentid = models.CharField(max_length=100,
                      verbose_name=u'Code de la structure père')
    parent = models.ForeignKey ('Structure', blank=True ,
                        null=True, related_name='fils',verbose_name=u'Lien direct vers la structure parent')

    ordre = models.CharField(max_length=100,verbose_name=u'Ordre')
    niv = models.CharField(max_length=100,verbose_name=u'Niveau')
    bloq = models.CharField(max_length=100,verbose_name=u'Bloqué')
    modifdate = models.CharField(max_length=100,default="", verbose_name=u'Date de modification')
    modifpar = models.CharField(max_length=100,verbose_name=u'Modifié par')
    dfmc = models.CharField(max_length=100,verbose_name=u'DFMC')
    fdr = models.CharField(max_length=100,verbose_name=u'FDR')
    ccassoc = models.CharField(max_length=100,blank=True , null = True,default="",verbose_name=u'CC associé')
    cpassoc = models.CharField(max_length=100,blank=True , null = True,default="",verbose_name=u'CP associé')

    class Meta: ordering = ['name']

    def __str__(self):
        return (self.name + " -- " + self.label)


"""----------------------------------------------
Gestion des Plans de financement. En cours de précisions
----------------------------------------------"""
#myid : code court pour l operation
#name : designation de l operation
class PlanFinancement(models.Model):
    myid = models.CharField(max_length=100, default='',blank=True,verbose_name=u'Code court')
    name = models.CharField(max_length=100,verbose_name=u'Libellé')
    eotp = models.CharField(max_length=100,
                        verbose_name=u'Code court de l\'eotp')
    creele = models.DateTimeField(auto_now_add = True, blank=True,
                        verbose_name=u'Date de création')
    creepar = models.CharField (max_length = 100 , blank=True , null = True,
                        verbose_name=u'Créé par')
    modifiele = models.DateTimeField(auto_now = True, blank=True,
                        verbose_name=u'Date de modification')
    modifiepar= models.CharField (max_length = 100 , blank=True , null = True,
                        verbose_name=u'Modification par')
    societe = models.CharField(max_length=100, default="",
                        verbose_name=u'Société')
    cfassoc = models.CharField(max_length=100,default="",
                        verbose_name=u'Centre financier associé')
    ccassoc = models.CharField(max_length=100, default="",
                        verbose_name=u'Centre de coût associé')
    cpassoc = models.CharField(max_length=100, default="",
                        verbose_name=u'Centre de profit associé')
    fleche = models.BooleanField(default=False,verbose_name=u'Fléché oui/non')
    pluriannuel = models.BooleanField(default=False,
                        verbose_name=u'Pluriannuel oui/non')

    cfassoclink = models.ForeignKey('Structure', blank=True ,
                        null=True,verbose_name=u'Lien direct vers le CF')

    class Meta: ordering = ['name'] 

    def __str__(self):
        return ("PFI:"+self.myid + " -- Eotp:" + self.eotp)



"""----------------------------------------------
Gestion des Depenses. En cours de précisions
----------------------------------------------"""
class DepenseFull ( models.Model ):
    myid = models.CharField(max_length=100, default='',blank=True)
    structlev3 = models.ForeignKey ('Structure',related_name='depensestructlev3',verbose_name=u'Structure-CF')
    cptdeplev1 = models.ForeignKey ('NatureComptable', blank=True , null=True,
                        related_name='depenses',verbose_name=u'Nature comptable')

    domfonc = models.ForeignKey ('DomaineFonctionnel' , blank = True ,
                        null = True,verbose_name=u'Domaine fonctionnel' )

    plfi = models.ForeignKey ( 'PlanFinancement' ,verbose_name=u'Programme de financement' )

    montant = models.CharField ( max_length = 100 ,blank = True , null = True )
    montantdc = models.DecimalField(max_digits=12, decimal_places=2 ,
                        blank = True , null = True )
    montantcp = models.DecimalField(max_digits=12, decimal_places=2 ,
                        blank = True , null = True )
    montantae = models.DecimalField(max_digits=12, decimal_places=2 ,
                        blank = True , null = True )
    dateae = models.DateField( blank = True , null = True )
    commentaire = models.CharField (max_length = 100 , blank=True , null = True)
    myfile =models.TextField(validators=[URLValidator()],blank=True, verbose_name=u'Lien vers un fichier')
    periodebudget = models.ForeignKey ('PeriodeBudget', blank=True ,
                        null=True, related_name='periodebudget1')
    creele = models.DateTimeField(auto_now_add = True,blank=True)
    creepar = models.CharField (max_length = 100 , blank=True , null = True)
    modifiele = models.DateTimeField(auto_now = True, blank=True, verbose_name=u'Date de modification')
    modifiepar= models.CharField (max_length = 100 , blank=True , null = True)


    def clean(self):
        montantae=self.montantae
        montantcp=self.montantcp

        if self.structlev3 :
            pass
        else:
            raise ValidationError({'structlev3':u'Veuillez choisir la structure'} )
        if not self.plfi :
            raise ValidationError({'plfi':u'Veuillez choisir le PFI'} )
        if self.cptdeplev1 :
            decalagetreso =self.cptdeplev1.decalagetresocpae
            if decalagetreso == False:
                if montantae != montantcp:
                    raise ValidationError({'montantae':u'Pas de décalage de trésorerie sur cette nature comptable.Veuillez vous assurrer que montantae=montantcp.'} )
        else:
            raise ValidationError({'cptdeplev1':u'Veuillez saisir la nature comptable'} )


    def save(self, *args, **kwargs):
        self.full_clean()
        super(DepenseFull, self).save(*args, **kwargs)


"""----------------------------------------------
Gestion des Recettes. En cours de précisions
----------------------------------------------"""
class RecetteFull ( models.Model ):
    myid = models.CharField(max_length=100, default='',blank=True)
    structlev3 = models.ForeignKey ('Structure',related_name='recstructlev3',verbose_name=u'Structure-CF')
    cptdeplev1 = models.ForeignKey ('NatureComptable',related_name='recettes',verbose_name=u'Nature comptable')
    domfonc = models.ForeignKey ('DomaineFonctionnel', verbose_name=u'Domaine fonctionnel')
    plfi = models.ForeignKey ( 'PlanFinancement', verbose_name=u'Programme de financement' )

    montant = models.DecimalField(max_digits=12, decimal_places=2 ,
                       blank = True , null = True )
    montantar = models.DecimalField(max_digits=12, decimal_places=2,
                       blank = True , null = True )
    montantre = models.DecimalField(max_digits=12, decimal_places=2,
                       blank = True , null = True )
    montantdc = models.DecimalField(max_digits=12, decimal_places=2,
                       blank = True , null = True )

    commentaire = models.CharField (max_length = 100 , blank=True , null = True)

    myfile =models.TextField(validators=[URLValidator()],blank=True,verbose_name=u'Lien vers un fichier')
    periodebudget = models.ForeignKey ('PeriodeBudget', blank=True , null=True,
                       related_name='periodebudget2')
    creele = models.DateTimeField(auto_now_add = True, blank =True)
    creepar = models.CharField (max_length = 100 , blank=True , null = True)
    modifiele = models.DateTimeField(auto_now = True,blank=True, verbose_name=u'Date de modification')
    modifiepar= models.CharField (max_length = 100 , blank=True , null = True)

    def clean (self):
        pass


    def save(self, *args, **kwargs):
        self.full_clean()
        super(RecetteFull, self).save(*args, **kwargs)



