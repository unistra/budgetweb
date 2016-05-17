from django import forms

from .models import Authorisation , CompteComptable , DomaineFonctionnel , OrigineFonds
from .models import Structure , PlanFinancement , Depense, DepenseFull , RecetteFull , PeriodeBudget
import json
from django.http import Http404,HttpResponse


""" *********************************
class Authorisation(models.Model):
    username = models.CharField(max_length=100)
    object = models.CharField(max_length=100)
**********************************  """

class AuthorisationForm(forms.ModelForm):

    class Meta:
        model = Authorisation
        fields = ( 'username' , 'object' )


""" **************************
class CompteComptable(models.Model):
    ccid = models.CharField(max_length=100)
    ccparent = models.CharField(max_length=100)
    ccname = models.CharField(max_length=100)
    cclabel = models.CharField(max_length=100)
    cctype = models.Charfield(max_length=100)
    ccinput = models.CharField(max_length=100)
    cctypectrl = models.CharField(max_length=100)
**************************** """

class CompteComptableForm(forms.ModelForm):

    class Meta:
        model = CompteComptable
        fields = ( 'ccid' , 'ccparent' , 'ccname' , 'cclabel' , 'cctype' , 'ccinput' , 'cctypectrl' )


""" ********************************************
class DomaineFonctionnel(models.Model):
    dfcode = models.CharField(max_length=100, default="")
    dflabel = models.CharField(max_length=100, default="")
    dfgrpcumul = models.CharField(max_length=100, default="")
    dfgrpfonc = models.CharField(max_length=100, default="")
    dfrmq = models.CharField(max_length=100, default="")
    dfdesc = models.CharField(max_length=100, default="")
********************************************** """

class DomaineFonctionnelForm(forms.ModelForm):

    class Meta:
        model = DomaineFonctionnel
        fields = ( 'dfcode' ,'dflabel' , 'dfgrpcumul' , 'dfgrpfonc' , 'dfrmq' , 'dfdesc' )



""" ************************************************
class OrigineFonds(models.Model):
    ofid = models.CharField(max_length=100)
    ofparent = models.CharField(max_length=100)
    ofname = models.CharField(max_length=100)
    oflabel = models.CharField(max_length=100)
    oftype = models.CharField(max_length=100)
    ofbudget = models.CharField(max_length=100)
    ofnomades = models.CharField(max_length=100)
************************************************ """
class OrigineFondsForm(forms.ModelForm):

    class Meta:
        model = OrigineFonds
        fields = ( 'ofid' , 'ofparent' , 'ofname' , 'oflabel' , 'oftype' , 'ofbudget' , 'ofnomades' )


""" **************************************************

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

*************************************************** """

class StructureForm( forms.ModelForm ):

    class Meta:
        model = Structure
        fields = ( 'myid' , 'type' , 'name' , 'label' , 'parentid' , 'ordre' , 'niv' ,
                   'bloq' , 'modifdate' , 'modifpar' , 'dfmc' , 'fdr' )


class StructureFormcc( forms.ModelForm ):

    class Meta:
        model = Structure
        fields = ( 'myid' , 'type' , 'name' , 'label' , 'parentid' , 'ordre' , 'niv' ,
                   'bloq' , 'modifdate' , 'modifpar' , 'dfmc' , 'fdr' )


    def __init__(self,*args,**kwargs):
        super (StructureFormcc,self ).__init__(*args,**kwargs) # populates the post
        self.fields['type'].queryset = " cc"



""" -----------------------------------------
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
---------------------------------------- """

class PlanFinancementForm( forms.ModelForm ):

    class Meta:
        model = PlanFinancement
        fields = ( 'myid' , 'name' , 'eotp', 'idabrege' , 'creepar' , 'creedate' , 'modifpar' , 'modifdate' , 'dem' , 'label' , 'type' , 'budget' , 'nomades' , 'refsifac' , 'refdfi' ,
                   'societe' , 'ccassoc' , 'cpassoc' , 'responsable' , 'dordre' ,
                   'divirecette' , 'status' , 'cleregul' , 'domainefonc')


""" -------------------------------------------------------
class Depense ( models.Model ):
    myid = models.CharField(max_length=100)
    struct = Structure()
    cptdep = CompteComptable()       
    domfonc = DomaineFonctionnel()           
    orfonds = OrigineFonds()        
    plfi = PlanFinancement()
    montant = models.CharField ( max_length = 100 )
    commentaire = models.CharField (max_length = 100)
------------------------------------------------------ """

class DepenseForm ( forms.ModelForm ):

    class Meta:
        model = Depense
        fields = ( 'myid' , 'struct' , 'cptdep' , 'domfonc' ,
                   'orfonds' , 'plfi' , 'montant' , 'commentaire' )


class DepenseForm2 ( forms.ModelForm ):

    class Meta:
        model = Depense
        fields = ( 'myid' , 'struct' , 'cptdep' , 'domfonc' ,
                   'orfonds' , 'plfi' , 'montant' , 'commentaire' )

    def __init__(self,*args,**kwargs):
        super (DepenseForm2,self ).__init__(*args,**kwargs) # populates the post
        self.fields['struct'].queryset = Structure.objects.filter(type=" cc")

""" ---------------------------------------------------
class DepenseFull ( models.Model ):
    myid = models.CharField(max_length=100)
    structlev1 = models.ForeignKey ('Structure',blank=True, null=True)
    structlev2 = models.ForeignKey ('Structure',blank=True, null=True)

    cptdeplev1 = models.ForeignKey ('CompteComptable', blank=True , null=True)
    cptdeplev2 = models.ForeignKey ('CompteComptable', blank=True , null=True)

    domfonc = models.ForeignKey ('DomaineFonctionnel' , blank = True , null = True )
    orfonds = models.ForeignKey ( 'OrigineFonds' , blank = True , null = True )
    plfi = models.ForeignKey ( 'PlanFinancement' , blank = True , null = True )
    montant = models.CharField ( max_length = 100 )
    commentaire = models.CharField (max_length = 100 , blank=True , null = True)

-------------------------------------------------------------------------------"""


class DepenseFullForm ( forms.ModelForm ):

    class Meta:
        model = DepenseFull
        fields = ( 'myid' , 'structlev1' , 'structlev2' ,'structlev3' , 'cptdeplev1' ,'cptdeplev2' , 'domfonc' ,
                   'orfonds' , 'orfonds' , 'plfi' , 'montant' , 'montantdc', 'montantcp' , 'montantae' , 'commentaire' , 'periodebudget' )


    def __init__(self,*args,**kwargs):
        super (DepenseFullForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['structlev1'].queryset = Structure.objects.filter(type=" cf")
        self.fields['cptdeplev1'].queryset = CompteComptable.objects.filter(cctype="dep",ccparent="1")



""" --------------------------------------------------------------
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
------------------------------------------------------------------------- """

class RecetteFullForm ( forms.ModelForm ):

    class Meta:
        model = RecetteFull
        fields = ( 'myid' , 'structlev1' , 'structlev2' ,'structlev3' , 'cptdeplev1' ,'cptdeplev2' , 'domfonc' ,
                   'orfonds' , 'orfonds' , 'plfi' , 'montant' , 'montantar', 'montantre' , 'commentaire' , 'periodebudget' )

    def __init__(self,*args,**kwargs):
        super (RecetteFullForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['structlev1'].queryset = Structure.objects.filter(type=' cf')
        self.fields['cptdeplev1'].queryset = CompteComptable.objects.filter(cctype='rec',ccparent="1")


""" -----------------
class PeriodeBudget(models.Model):
    name = models.CharField(max_length=20)
    label = models.CharField(max_length=100)
    annee = models.DateField( null=True)
    bloque = models.BooleanField(default = True)
--------------------------------------"""
class PeriodeBudgetForm (forms.ModelForm):

    class Meta:
        model = PeriodeBudget
        fields = ('name' , 'label' , 'annee' , 'bloque')



