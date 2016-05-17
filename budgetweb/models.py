from django.db import models
from django import forms

from django.utils import timezone
import operator

from django.db.models import Q
from datetime import datetime


class Authorisation(models.Model):
    username = models.CharField(max_length=100)
    object = models.CharField(max_length=100)


class PeriodeBudget(models.Model):
    name = models.CharField(max_length=20)
    label = models.CharField(max_length=100)
    annee = models.DateField( null=True)
    bloque = models.BooleanField(default = True)

    def __str__(self):
        return (self.name + " -- " + self.label + " -- " + str(self.annee.year))


class CompteComptable(models.Model):
    ccid = models.CharField(max_length=100)
    ccparent = models.CharField(max_length=100)
    ccname = models.CharField(max_length=100)
    cclabel = models.CharField(max_length=100)
    cctype = models.CharField(max_length=100)
    ccinput = models.CharField(max_length=100)
    cctypectrl = models.CharField(max_length=100)

    def __str__(self):
        return (self.ccname + " -- " + self.cclabel)


class DomaineFonctionnel(models.Model):
    dfcode = models.CharField(max_length=100, default="")
    dflabel = models.CharField(max_length=100, default="")
    dfgrpcumul = models.CharField(max_length=100, default="")
    dfgrpfonc = models.CharField(max_length=100, default="")
    dfrmq = models.CharField(max_length=100, default="")
    dfdesc = models.CharField(max_length=100, default="")

    def __str__(self):
        return (self.dfcode + " -- " + self.dflabel)



class OrigineFonds(models.Model):
    ofid = models.CharField(max_length=100)
    ofparent = models.CharField(max_length=100)
    ofname = models.CharField(max_length=100)
    oflabel = models.CharField(max_length=100)
    oftype = models.CharField(max_length=100)
    ofbudget = models.CharField(max_length=100)
    ofnomades = models.CharField(max_length=100)

    def __str__(self):
        return (self.ofname + " -- " + self.ofid)


class Structure(models.Model):
    myid = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    parentid = models.CharField(max_length=100)
    ordre = models.CharField(max_length=100)
    niv = models.CharField(max_length=100)
    bloq = models.CharField(max_length=100)
    modifdate = models.CharField(max_length=100)
    modifpar = models.CharField(max_length=100)
    dfmc = models.CharField(max_length=100)
    fdr = models.CharField(max_length=100)

    def __str__(self):
        return (self.name + " -- " + self.label)


class PlanFinancement(models.Model):
    myid = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    eotp = models.CharField(max_length=100)
    idabrege = models.CharField(max_length=100)
    creepar =models.CharField(max_length=100)
    creedate = models.CharField(max_length=100)
    modifpar = models.CharField(max_length=100)
    modifdate = models.CharField(max_length=100)
    dem = models.CharField(max_length=100)
    label  = models.CharField(max_length=100)
    type   = models.CharField(max_length=100)
    budget = models.CharField(max_length=100)
    nomades= models.CharField(max_length=100)
    refsifac= models.CharField(max_length=100, default="")
    refdfi  = models.CharField(max_length=100, default="")
    societe = models.CharField(max_length=100, default="")
    ccassoc = models.CharField(max_length=100, default="")
    cpassoc = models.CharField(max_length=100, default="")
    responsable = models.CharField(max_length=100, default="") 
    dordre = models.CharField(max_length=100, default="")
    divirecette = models.CharField(max_length=100, default="")
    status = models.CharField(max_length=100, default="")
    cleregul = models.CharField(max_length=100, default="")
    domainefonc = models.CharField(max_length=100, default="")

    def __str__(self):
        return (self.name + " -- " + self.eotp)


class Depense ( models.Model ):
    myid = models.CharField(max_length=100)
    struct = models.ForeignKey ('Structure',blank=True, null=True)
    cptdep = models.ForeignKey ('CompteComptable', blank=True , null=True) 
    domfonc = models.ForeignKey ('DomaineFonctionnel' , blank = True , null = True ) 
    orfonds = models.ForeignKey ( 'OrigineFonds' , blank = True , null = True ) 
    plfi = models.ForeignKey ( 'PlanFinancement' , blank = True , null = True )
    montant = models.CharField ( max_length = 100 )
    commentaire = models.CharField (max_length = 100 , blank=True , null = True)


class DepenseFull ( models.Model ):
    myid = models.CharField(max_length=100)
    structlev1 = models.ForeignKey ('Structure',blank=True, null=True, related_name='structlev1')
    structlev2 = models.ForeignKey ('Structure',blank=True, null=True, related_name='structlev2')
    structlev3 = models.ForeignKey ('Structure',blank=True, null=True, related_name='structlev3')

    cptdeplev1 = models.ForeignKey ('CompteComptable', blank=True , null=True, related_name='cptdeplev1')
    cptdeplev2 = models.ForeignKey ('CompteComptable', blank=True , null=True, related_name='cptdeplev2')

    domfonc = models.ForeignKey ('DomaineFonctionnel' , blank = True , null = True )
    orfonds = models.ForeignKey ( 'OrigineFonds' , blank = True , null = True , related_name='orfonds')
    orfonds2 = models.ForeignKey ( 'OrigineFonds' , blank = True , null = True , related_name='orfonds2')
    plfi = models.ForeignKey ( 'PlanFinancement' , blank = True , null = True )
    montant = models.CharField ( max_length = 100 ,blank = True , null = True )
    montantdc = models.DecimalField(max_digits=12, decimal_places=2 , blank = True , null = True )
    montantcp = models.DecimalField(max_digits=12, decimal_places=2 , blank = True , null = True )
    montantae = models.DecimalField(max_digits=12, decimal_places=2 , blank = True , null = True )
    dateae = models.DateField( blank = True , null = True )
    commentaire = models.CharField (max_length = 100 , blank=True , null = True)

    myfile = forms.FileField()
    periodebudget = models.ForeignKey ('PeriodeBudget', blank=True , null=True, related_name='periodebudget1')
    creele = models.DateTimeField(auto_now_add = True,blank=True) # default=datetime.now())
    creepar = models.CharField (max_length = 100 , blank=True , null = True)
    modifiele = models.DateTimeField(auto_now = True, blank=True) #default=datetime.now())
    modifiepar= models.CharField (max_length = 100 , blank=True , null = True)




class RecetteFull ( models.Model ):
    myid = models.CharField(max_length=100)
    structlev1 = models.ForeignKey ('Structure',blank=True, null=True, related_name='recstructlev1')
    structlev2 = models.ForeignKey ('Structure',blank=True, null=True, related_name='recstructlev2')
    structlev3 = models.ForeignKey ('Structure',blank=True, null=True, related_name='recstructlev3')

    cptdeplev1 = models.ForeignKey ('CompteComptable', blank=True , null=True, related_name='reccptdeplev1')
    cptdeplev2 = models.ForeignKey ('CompteComptable', blank=True , null=True, related_name='reccptdeplev2')

    domfonc = models.ForeignKey ('DomaineFonctionnel' , blank = True , null = True )
    orfonds = models.ForeignKey ( 'OrigineFonds' , blank = True , null = True , related_name='recorfonds')
    orfonds2 = models.ForeignKey ( 'OrigineFonds' , blank = True , null = True , related_name='recorfonds2')
    plfi = models.ForeignKey ( 'PlanFinancement' , blank = True , null = True )

    montant = models.DecimalField(max_digits=12, decimal_places=2 , blank = True , null = True )
    montantar = models.DecimalField(max_digits=12, decimal_places=2 , blank = True , null = True )
    montantre = models.DecimalField(max_digits=12, decimal_places=2 , blank = True , null = True )
    commentaire = models.CharField (max_length = 100 , blank=True , null = True)

    myfile = forms.FileField()
    periodebudget = models.ForeignKey ('PeriodeBudget', blank=True , null=True, related_name='periodebudget2')
    creele = models.DateTimeField(auto_now_add = True, blank =True)
    creepar = models.CharField (max_length = 100 , blank=True , null = True)
    modifiele = models.DateTimeField(auto_now = True,blank=True)
    modifiepar= models.CharField (max_length = 100 , blank=True , null = True)

# -------  a voire ----------------

class AdresseBudgetaire(models.Model):
    myid = models.CharField(max_length=100)
    parent = models.CharField(max_length=100)
    name   = models.CharField(max_length=100)
    label  = models.CharField(max_length=100)
    type   = models.CharField(max_length=100)
    compta = models.CharField(max_length=100)
    budget = models.CharField(max_length=100)
    lolf   = models.CharField(max_length=100)
    a      = models.CharField(max_length=100)


class MasseMouvementees(models.Model):
    myid = models.CharField(max_length=100)
    parent = models.CharField(max_length=100)
    name   = models.CharField(max_length=100)
    label  = models.CharField(max_length=100)
    rd     = models.CharField(max_length=100)
    input  = models.CharField(max_length=100)
    typecontrole = models.CharField(max_length=100)


 
class CompteBudgetaire(models.Model):
    code = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


