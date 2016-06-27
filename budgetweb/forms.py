from django import forms

from .models import Authorisation , CompteBudget, NatureComptable , DomaineFonctionnel
from .models import Structure , PlanFinancement , DepenseFull , RecetteFull , PeriodeBudget
from .models import FondBudgetaire, ComptaNature

import json
from django.http import Http404,HttpResponse



class AuthorisationForm(forms.ModelForm):

    class Meta:
        model = Authorisation
        fields = ( 'username' , 'myobject' )


class CompteBudgetForm(forms.ModelForm):

    class Meta:
        model = CompteBudget
        fields = ('code','label','description')

class ComptaNatureForm(forms.ModelForm):

    class Meta:
        model = ComptaNature
        fields = ('code','label')


class FondBudgetaireForm(forms.ModelForm):

    class Meta:
        model = FondBudgetaire
        fields = ('code','label')


class NatureComptableForm(forms.ModelForm):

    class Meta:
        model = NatureComptable
        fields = ( 'enveloppe', 'fondbudget_recette' , 'naturec_dep' , 'pfifleche' , 'ncsecondairecode' ,
                   'ccbd' , 'decalagetresocpae','nctype')

        #widgets = {
        #    'nclabel': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
        #}



class DomaineFonctionnelForm(forms.ModelForm):

    class Meta:
        model = DomaineFonctionnel
        fields = ( 'dfcode' ,'dflabel' , 'dfgrpcumul' , 'dfgrpfonc' , 'dfrmq' , 'dfdesc' )





class StructureForm( forms.ModelForm ):

    class Meta:
        model = Structure
        fields = ( 'myid' , 'type' , 'name' , 'label' , 'parentid' , 'ordre' , 'niv' ,
                   'bloq' , 'modifdate' , 'modifpar' , 'dfmc' , 'fdr', 'parent' )


class StructureFormcc( forms.ModelForm ):

    class Meta:
        model = Structure
        fields = ( 'myid' , 'type' , 'name' , 'label' , 'parentid' , 'ordre' , 'niv' ,
                   'bloq' , 'modifdate' , 'modifpar' , 'dfmc' , 'fdr' )


    def __init__(self,*args,**kwargs):
        super (StructureFormcc,self ).__init__(*args,**kwargs) # populates the post
        self.fields['type'].queryset = " cc"




class PlanFinancementForm( forms.ModelForm ):

    class Meta:
        model = PlanFinancement
        fields = ( 'myid' , 'name' , 'eotp', 'creepar' , 'modifiepar' , 
                   'societe' , 'cfassoc' , 'ccassoc' , 'cpassoc' , 'fleche' , 'pluriannuel', 'cfassoclink')

        widgets = {
            'name': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
        }



class DepenseFullForm ( forms.ModelForm ):

    class Meta:
        model = DepenseFull
        fields = ( 'myid' , 'structlev1' , 'structlev2' ,'structlev3' , 'cptdeplev1', 'domfonc' ,
                   'plfi' , 'montant' , 'montantdc', 'montantcp' , 'montantae' , 'commentaire' , 'periodebudget' )


    def __init__(self,*args,**kwargs):
        super (DepenseFullForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['structlev1'].queryset = Structure.objects.filter(type=" cf").order_by('name')
        #self.fields['cptdeplev1'].queryset = NatureComptable.objects.filter(nctype='dep').order_by('naturec_dep')
        #-----
        instance = getattr(self, 'instance', None)
        #pas de modification sur ces champs
        # la periode de budget est calculee automatiquement 
        if instance and instance.pk:
            self.fields['structlev1'].widget.attrs['readonly'] = True
            self.fields['structlev1'].widget.attrs['disabled'] = 'disabled'
            self.fields['structlev2'].widget.attrs['readonly'] = True
            self.fields['structlev2'].widget.attrs['disabled'] = 'disabled'
            self.fields['structlev3'].widget.attrs['readonly'] = True
            self.fields['structlev3'].widget.attrs['disabled'] = 'disabled'
            self.fields['cptdeplev1'].widget.attrs['readonly'] = True
            self.fields['cptdeplev1'].widget.attrs['disabled'] = 'disabled'
            self.fields['plfi'].widget.attrs['readonly'] = True
            self.fields['plfi'].widget.attrs['disabled'] = 'disabled'
            self.fields['myid'].widget.attrs['readonly'] = True
            self.fields['myid'].widget.attrs['disabled'] = 'disabled'

            self.fields['periodebudget'].widget.attrs['readonly'] = True
            self.fields['domfonc'].widget.attrs['readonly'] = True
            self.fields['domfonc'].widget.attrs['disabled'] = 'disabled'
            self.fields['periodebudget'].widget.attrs['disabled'] = 'disabled'

    def clean_structlev1(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.structlev1
        else:
            return self.cleaned_data['structlev1']

    def clean_myid(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.myid
        else:
            return self.cleaned_data['myid']


class RecetteFullForm ( forms.ModelForm ):

    class Meta:
        model = RecetteFull
        fields = ( 'myid' , 'structlev1' , 'structlev2' ,'structlev3' , 'cptdeplev1' , 'domfonc' ,
                   'plfi' , 'montant' , 'montantar', 'montantre' ,'montantdc', 'commentaire' , 'periodebudget' )

    def __init__(self,*args,**kwargs):
        super (RecetteFullForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['structlev1'].queryset = Structure.objects.filter(type=' cf')
        self.fields['cptdeplev1'].queryset = NatureComptable.objects.filter(nctype='rec')

        instance = getattr(self, 'instance', None)
        #pas de modification sur ces champs
        # en recette domfonc=NA toujours
        # la periode de budget est calculee automatiquement 
        if instance and instance.pk:
            self.fields['structlev1'].widget.attrs['readonly'] = True
            self.fields['structlev1'].widget.attrs['disabled'] = 'disabled'
            self.fields['structlev2'].widget.attrs['readonly'] = True
            self.fields['structlev2'].widget.attrs['disabled'] = 'disabled'
            self.fields['structlev3'].widget.attrs['readonly'] = True
            self.fields['structlev3'].widget.attrs['disabled'] = 'disabled'
            self.fields['cptdeplev1'].widget.attrs['readonly'] = True
            self.fields['cptdeplev1'].widget.attrs['disabled'] = 'disabled'
            self.fields['plfi'].widget.attrs['readonly'] = True
            self.fields['plfi'].widget.attrs['disabled'] = 'disabled'
            self.fields['myid'].widget.attrs['readonly'] = True
            self.fields['myid'].widget.attrs['disabled'] = 'disabled'

            self.fields['periodebudget'].widget.attrs['readonly'] = True
            self.fields['domfonc'].widget.attrs['readonly'] = True
            self.fields['domfonc'].widget.attrs['disabled'] = 'disabled'
            self.fields['periodebudget'].widget.attrs['disabled'] = 'disabled'


class PeriodeBudgetForm (forms.ModelForm):

    class Meta:
        model = PeriodeBudget
        fields = ('name' , 'label' , 'annee' , 'bloque')



