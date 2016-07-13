from django import forms
from django.forms.formsets import BaseFormSet
from django.forms.models import modelformset_factory, BaseModelFormSet
from django.http import Http404, HttpResponse

#from .models import (Authorisation, ComptaNature, CompteBudget, DepenseFull,
#                     DomaineFonctionnel, FondBudgetaire, NatureComptable,
#                     PeriodeBudget, PlanFinancement, RecetteFull, Structure)


#class AuthorisationForm(forms.ModelForm):
#
#    class Meta:
#        model = Authorisation
#        fields = ('username', 'myobject')
#
#
#class CompteBudgetForm(forms.ModelForm):
#
#    class Meta:
#        model = CompteBudget
#        fields = ('code', 'label', 'description')
#
#
#class ComptaNatureForm(forms.ModelForm):
#
#    class Meta:
#        model = ComptaNature
#        fields = ('code', 'label')
#
#
#class FondBudgetaireForm(forms.ModelForm):
#
#    class Meta:
#        model = FondBudgetaire
#        fields = ('code', 'label')
#
#
#class NatureComptableForm(forms.ModelForm):
#
#    class Meta:
#        model = NatureComptable
#        fields = ('enveloppe', 'fondbudget_recette', 'naturec_dep',
#                  'pfifleche', 'ncsecondairecode', 'ccbd', 'decalagetresocpae',
#                  'nctype')
#
#
#class DomaineFonctionnelForm(forms.ModelForm):
#
#    class Meta:
#        model = DomaineFonctionnel
#        fields = ('dfcode', 'dflabel', 'dfgrpcumul', 'dfgrpfonc', 'dfrmq',
#                  'dfdesc')
#
#
#class StructureForm(forms.ModelForm):
#
#    class Meta:
#        model = Structure
#        fields = ('myid', 'type', 'name', 'label', 'parentid', 'ordre', 'niv',
#                  'bloq', 'modifdate', 'modifpar', 'dfmc', 'fdr', 'parent')
#
#
#class StructureFormcc(forms.ModelForm):
#
#    class Meta:
#        model = Structure
#        fields = ('myid', 'type', 'name', 'label', 'parentid', 'ordre', 'niv',
#                  'bloq', 'modifdate', 'modifpar', 'dfmc', 'fdr')
#
#    def __init__(self, *args, **kwargs):
#        # populates the post
#        super(StructureFormcc, self).__init__(*args, **kwargs)
#        self.fields['type'].queryset = " cc"
#
#
#class PlanFinancementForm(forms.ModelForm):
#
#    class Meta:
#        model = PlanFinancement
#        fields = ('myid', 'name', 'eotp', 'creepar', 'modifiepar', 'societe',
#                  'cfassoc', 'ccassoc', 'cpassoc', 'fleche', 'pluriannuel',
#                  'cfassoclink')
#
#        widgets = {
#            'name': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
#        }
#
#    def __init__(self, *args, **kwargs):
#        # populates the post
#        super(PlanFinancementForm, self).__init__(*args, **kwargs)
#        self.fields['cfassoclink'].queryset = Structure.objects\
#            .filter(type=' cf').order_by('name')
#
#
#class DepenseFullForm(forms.ModelForm):
#
#    class Meta:
#        model = DepenseFull
#        fields = ('id', 'myid', 'structlev3', 'cptdeplev1', 'domfonc', 'plfi',
#                  'montantdc', 'montantcp', 'montantae', 'dateae',
#                  'commentaire', 'periodebudget', 'myfile')
#
#        widgets = {
#            'myfile': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
#        }
#
#    def __init__(self, *args, **kwargs):
#        # populates the post
#        super(DepenseFullForm, self).__init__(*args, **kwargs)
#        #self.fields['structlev1'].queryset = Structure.objects\
##            .filter(type=" cf").order_by('name')
#        #self.fields['cptdeplev1'].queryset = NatureComptable.objects\
##            .filter(nctype='dep').order_by('naturec_dep')
#        #-----
#        instance = getattr(self, 'instance', None)
#        #pas de modification sur ces champs
#        # la periode de budget est calculee automatiquement
#        if instance and instance.pk:
#            self.fields['structlev3'].widget.attrs['readonly'] = True
#            self.fields['structlev3'].widget.attrs['disabled'] = 'disabled'
#            #self.fields['cptdeplev1'].widget.attrs['readonly'] = True
#            #self.fields['cptdeplev1'].widget.attrs['disabled'] = 'disabled'
#            self.fields['plfi'].widget.attrs['readonly'] = True
#            self.fields['plfi'].widget.attrs['disabled'] = 'disabled'
#            self.fields['myid'].widget.attrs['readonly'] = True
#            self.fields['myid'].widget.attrs['disabled'] = 'disabled'
#            self.fields['periodebudget'].widget.attrs['readonly'] = True
#            #self.fields['domfonc'].widget.attrs['readonly'] = True
#            #self.fields['domfonc'].widget.attrs['disabled'] = 'disabled'
#            self.fields['periodebudget'].widget.attrs['disabled'] = 'disabled'
#
#    def clean_myid(self):
#        instance = getattr(self, 'instance', None)
#        if instance and instance.pk:
#            return instance.myid
#        else:
#            return self.cleaned_data['myid']
#
#
#class DepenseFullFormRestrict (forms.ModelForm):
#
#    class Meta:
#        model = DepenseFull
#        fields = ('id', 'structlev3', 'cptdeplev1', 'domfonc', 'plfi',
#                  'montantdc', 'montantcp', 'montantae', 'dateae',
#                  'commentaire', 'myfile')
#
#        widgets = {
#            'myfile': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
#        }
#
#    def __init__(self, *args, **kwargs):
#        super(DepenseFullFormRestrict, self).__init__(*args, **kwargs)
#        instance = getattr(self, 'instance', None)
#        #pas de modification sur ces champs
#        self.fields['cptdeplev1'].queryset = NatureComptable.objects.filter(
#            id=instance.cptdeplev1.id)
#        self.fields['structlev3'].queryset = Structure.objects.filter(
#            id=instance.structlev3.id)
#        self.fields['plfi'].queryset = PlanFinancement.objects.filter(
#            id=instance.plfi.id)
#
#
#class DepenseFullFormPfifleche(forms.ModelForm):
#
#    class Meta:
#        model = DepenseFull
#        fields = ('id', 'myid', 'structlev3', 'cptdeplev1', 'domfonc', 'plfi',
#                  'montantdc', 'montantcp', 'montantae', 'dateae',
#                  'commentaire', 'periodebudget', 'myfile')
#
#        widgets = {
#            'myfile': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
#        }
#
#    def __init__(self, *args, **kwargs):
#        super(DepenseFullFormPfifleche, self).__init__(*args, **kwargs)
#        self.fields['cptdeplev1'].queryset = NatureComptable.objects.filter(
#            nctype='dep', pfifleche=True).order_by('enveloppe')
#
#        instance = getattr(self, 'instance', None)
#        #pas de modification sur ces champs
#        #self.fields['cptdeplev1'].queryset = NatureComptable.objects.filter(id=instance.cptdeplev1.id)
#        #self.fields['structlev3'].queryset = Structure.objects.filter(id=instance.structlev3.id)
#        #self.fields['plfi'].queryset = PlanFinancement.objects.filter(id=instance.plfi.id)
#
#        #pas de modification sur ces champs
#        # la periode de budget est calculee automatiquement 
#        if instance and instance.pk:
#            self.fields['structlev3'].queryset = Structure.objects.filter(id=instance.structlev3.id)
#            self.fields['plfi'].queryset = PlanFinancement.objects.filter(id=instance.plfi.id)
#            #self.fields['structlev3'].widget.attrs['readonly'] = True
#            #self.fields['structlev3'].widget.attrs['disabled'] = 'disabled'
#            #self.fields['cptdeplev1'].widget.attrs['readonly'] = True
#            #self.fields['cptdeplev1'].widget.attrs['disabled'] = 'disabled'
#            #self.fields['plfi'].widget.attrs['readonly'] = True
#            #self.fields['plfi'].widget.attrs['disabled'] = 'disabled'
#            self.fields['myid'].widget.attrs['readonly'] = True
#            self.fields['myid'].widget.attrs['disabled'] = 'disabled'
#            self.fields['periodebudget'].widget.attrs['readonly'] = True
#            #self.fields['domfonc'].widget.attrs['readonly'] = True
#            #self.fields['domfonc'].widget.attrs['disabled'] = 'disabled'
#            self.fields['periodebudget'].widget.attrs['disabled'] = 'disabled'
#
#    def clean_myid(self):
#        instance = getattr(self, 'instance', None)
#        if instance and instance.pk:
#            return instance.myid
#        else:
#            return self.cleaned_data['myid']
#
#
#class DepenseFullFormPfinonfleche(forms.ModelForm):
#
#    class Meta:
#        model = DepenseFull
#        fields = ('id', 'myid', 'structlev3', 'cptdeplev1', 'domfonc', 'plfi',
#                  'montantdc', 'montantcp', 'montantae', 'dateae',
#                  'commentaire', 'periodebudget', 'myfile')
#
#        widgets = {
#            'myfile': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
#        }
#
#    def __init__(self, *args, **kwargs):
#        super(DepenseFullFormPfinonfleche, self ).__init__(*args, **kwargs)
#        self.fields['cptdeplev1'].queryset = NatureComptable.objects.filter(
#            nctype='dep', pfifleche=False).order_by('enveloppe')
#
#        #-----
#        instance = getattr(self, 'instance', None)
#        #pas de modification sur ces champs
#        #self.fields['cptdeplev1'].queryset = NatureComptable.objects.filter(id=instance.cptdeplev1.id)
#        #self.fields['structlev3'].queryset = Structure.objects.filter(id=instance.structlev3.id)
#        #self.fields['plfi'].queryset = PlanFinancement.objects.filter(id=instance.plfi.id)
#
#        #pas de modification sur ces champs
#        # la periode de budget est calculee automatiquement 
#        if instance and instance.pk:
#            self.fields['structlev3'].queryset = Structure.objects.filter(id=instance.structlev3.id)
#            self.fields['plfi'].queryset = PlanFinancement.objects.filter(id=instance.plfi.id)
#
#            #self.fields['structlev3'].widget.attrs['readonly'] = True
#            #self.fields['structlev3'].widget.attrs['disabled'] = 'disabled'
#            #self.fields['cptdeplev1'].widget.attrs['readonly'] = True
#            #self.fields['cptdeplev1'].widget.attrs['disabled'] = 'disabled'
#            #self.fields['plfi'].widget.attrs['readonly'] = True
#            #self.fields['plfi'].widget.attrs['disabled'] = 'disabled'
#            self.fields['myid'].widget.attrs['readonly'] = True
#            self.fields['myid'].widget.attrs['disabled'] = 'disabled'
#            self.fields['periodebudget'].widget.attrs['readonly'] = True
#            #self.fields['domfonc'].widget.attrs['readonly'] = True
#            #self.fields['domfonc'].widget.attrs['disabled'] = 'disabled'
#            self.fields['periodebudget'].widget.attrs['disabled'] = 'disabled'
#
#    def clean_myid(self):
#        instance = getattr(self, 'instance', None)
#        if instance and instance.pk:
#            return instance.myid
#        else:
#            return self.cleaned_data['myid']
#
#
#class RecetteFullForm(forms.ModelForm):
#
#    class Meta:
#        model = RecetteFull
#        fields = ('myid', 'structlev3', 'cptdeplev1', 'domfonc', 'plfi',
#                  'montantar', 'montantre', 'montantdc', 'commentaire',
#                  'periodebudget', 'myfile')
#
#        widgets = {
#            'myfile': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
#        }
#
#    def __init__(self, *args, **kwargs):
#        super(RecetteFullForm, self ).__init__(*args, **kwargs)
#        self.fields['cptdeplev1'].queryset = NatureComptable.objects.filter(nctype='rec')
#        #en recette le DF = NA
#        self.fields['domfonc'].queryset = DomaineFonctionnel.objects.filter(dfcode='NA')
#        instance = getattr(self, 'instance', None)
#        #pas de modification sur ces champs
#        # en recette domfonc=NA toujours
#        # la periode de budget est calculee automatiquement
#        if instance and instance.pk:
#            self.fields['structlev3'].widget.attrs['readonly'] = True
#            self.fields['structlev3'].widget.attrs['disabled'] = 'disabled'
#            self.fields['cptdeplev1'].widget.attrs['readonly'] = True
#            self.fields['cptdeplev1'].widget.attrs['disabled'] = 'disabled'
#            self.fields['plfi'].widget.attrs['readonly'] = True
#            self.fields['plfi'].widget.attrs['disabled'] = 'disabled'
#            self.fields['myid'].widget.attrs['readonly'] = True
#            self.fields['myid'].widget.attrs['disabled'] = 'disabled'
#
#            self.fields['periodebudget'].widget.attrs['readonly'] = True
#            self.fields['domfonc'].widget.attrs['readonly'] = True
#            self.fields['domfonc'].widget.attrs['disabled'] = 'disabled'
#            self.fields['periodebudget'].widget.attrs['disabled'] = 'disabled'
#
#
#class RecetteFullFormRestrict(forms.ModelForm):
#
#    class Meta:
#        model = RecetteFull
#        fields = ('structlev3', 'cptdeplev1', 'domfonc', 'plfi', 'montantar',
#                  'montantre', 'montantdc', 'commentaire', 'myfile')
#
#        widgets = {
#            'myfile': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
#        }
#
#    def __init__(self, *args, **kwargs):
#        super(RecetteFullFormRestrict, self).__init__(*args, **kwargs)
#        instance = getattr(self, 'instance', None)
#        df_rec_na_set = DomaineFonctionnel.objects.filter(dfcode='NA')
#        #pas de modification sur ces champs
#        self.fields['cptdeplev1'].queryset = NatureComptable.objects.filter(id=instance.cptdeplev1.id)
#        self.fields['structlev3'].queryset = Structure.objects.filter(id=instance.structlev3.id)
#        self.fields['plfi'].queryset = PlanFinancement.objects.filter(id=instance.plfi.id)
#        self.fields['domfonc'].queryset = DomaineFonctionnel.objects.filter(dfcode='NA') #DomaineFonctionnel.objects.filter(id=instance.plfi.id)
#
#
#class RecetteFullFormPfifleche (forms.ModelForm):
#
#    class Meta:
#        model = RecetteFull
#        fields = ('myid', 'structlev3', 'cptdeplev1', 'domfonc', 'plfi',
#                  'montantar', 'montantre', 'montantdc', 'commentaire',
#                  'periodebudget', 'myfile')
#
#        widgets = {
#            'myfile': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
#        }
#
#    def __init__(self, *args, **kwargs):
#        super(RecetteFullFormPfifleche, self).__init__(*args, **kwargs)
#        self.fields['cptdeplev1'].queryset = NatureComptable.objects.filter(nctype='rec',pfifleche=True)
#        self.fields['domfonc'].queryset = DomaineFonctionnel.objects.filter(dfcode='NA')
#
#        instance = getattr(self, 'instance', None)
#        #pas de modification sur ces champs
#        # en recette domfonc=NA toujours
#        # la periode de budget est calculee automatiquement 
#        if instance and instance.pk:
#            self.fields['structlev3'].queryset = Structure.objects.filter(id=instance.structlev3.id)
#            self.fields['plfi'].queryset = PlanFinancement.objects.filter(id=instance.plfi.id)
#            #self.fields['domfonc'].queryset = DomaineFonctionnel.objects.filter(id=instance.plfi.id)
#            self.fields['cptdeplev1'].queryset = NatureComptable.objects.filter(id=instance.cptdeplev1.id)
#            #self.fields['structlev3'].widget.attrs['readonly'] = True
#            #self.fields['structlev3'].widget.attrs['disabled'] = 'disabled'
#            #self.fields['cptdeplev1'].widget.attrs['readonly'] = True
#            #self.fields['cptdeplev1'].widget.attrs['disabled'] = 'disabled'
#            #self.fields['plfi'].widget.attrs['readonly'] = True
#            #self.fields['plfi'].widget.attrs['disabled'] = 'disabled'
#            #self.fields['myid'].widget.attrs['readonly'] = True
#            #self.fields['myid'].widget.attrs['disabled'] = 'disabled'
#
#            self.fields['periodebudget'].widget.attrs['readonly'] = True
#            #self.fields['domfonc'].widget.attrs['readonly'] = True
#            #self.fields['domfonc'].widget.attrs['disabled'] = 'disabled'
#            self.fields['periodebudget'].widget.attrs['disabled'] = 'disabled'
#
#
#class RecetteFullFormPfinonfleche(forms.ModelForm):
#
#    class Meta:
#        model = RecetteFull
#        fields = ('myid', 'structlev3', 'cptdeplev1', 'domfonc', 'plfi',
#                  'montantar', 'montantre', 'montantdc', 'commentaire',
#                  'periodebudget', 'myfile')
#
#        widgets = {
#            'myfile': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
#        }
#
#    def __init__(self, *args, **kwargs):
#        super(RecetteFullFormPfinonfleche, self ).__init__(*args, **kwargs)
#        self.fields['cptdeplev1'].queryset = NatureComptable.objects.filter(nctype='rec',pfifleche=False)
#        self.fields['domfonc'].queryset = DomaineFonctionnel.objects.filter(dfcode='NA')
#        instance = getattr(self, 'instance', None)
#        #pas de modification sur ces champs
#        #self.fields['cptdeplev1'].queryset = NatureComptable.objects.filter(id=instance.cptdeplev1.id)
#
#        instance = getattr(self, 'instance', None)
#        #pas de modification sur ces champs
#        # en recette domfonc=NA toujours
#        # la periode de budget est calculee automatiquement 
#        if instance and instance.pk:
#            self.fields['structlev3'].queryset = Structure.objects.filter(id=instance.structlev3.id)
#            self.fields['plfi'].queryset = PlanFinancement.objects.filter(id=instance.plfi.id)
#
#            self.fields['cptdeplev1'].queryset = NatureComptable.objects.filter(id=instance.cptdeplev1.id)
#            #self.fields['structlev3'].widget.attrs['readonly'] = True
#            #self.fields['structlev3'].widget.attrs['disabled'] = 'disabled'
#            #self.fields['cptdeplev1'].widget.attrs['readonly'] = True
#            #self.fields['cptdeplev1'].widget.attrs['disabled'] = 'disabled'
#            #self.fields['plfi'].widget.attrs['readonly'] = True
#            #self.fields['plfi'].widget.attrs['disabled'] = 'disabled'
#            #self.fields['myid'].widget.attrs['readonly'] = True
#            #self.fields['myid'].widget.attrs['disabled'] = 'disabled'
#
#            self.fields['periodebudget'].widget.attrs['readonly'] = True
#            #self.fields['domfonc'].widget.attrs['readonly'] = True
#            #self.fields['domfonc'].widget.attrs['disabled'] = 'disabled'
#            self.fields['periodebudget'].widget.attrs['disabled'] = 'disabled'
#
#
#class PeriodeBudgetForm (forms.ModelForm):
#
#    class Meta:
#        model = PeriodeBudget
#        fields = ('name', 'label', 'annee', 'bloque')
#
#
#class BaseDepenseFullFormSet(BaseModelFormSet):
#
#    def clean(self):
#        if any(self.errors):
#            return
#
#        for form in self.forms:
#            if form.cleaned_data:
#                if 1:  # form.cleaned_data['myid']:
#                    montantae = form.cleaned_data['montantae']
#                    if not montantae:
#                        raise forms.ValidationError(
#                            'Veuillez renseigner montantae.',
#                            code='on_save_missing_montantae'
#                        )
#
#                    montantcp = form.cleaned_data['montantcp']
#                    if not montantcp:
#                        raise forms.ValidationError(
#                            'Veuillez renseigner montantcp.',
#                            code='on_save_missing_montantcp'
#                       )
#                    montantdc = form.cleaned_data['montantdc']
#                    if not montantdc:
#                        raise forms.ValidationError(
#                            'Veuillez renseigner montantdc.',
#                            code='on_save_missing_montantdc'
#                       )
#                    domfonc = form.cleaned_data['domfonc']
#                    if not domfonc:
#                        raise forms.ValidationError(
#                            'Veuillez renseigner le domaine fonctionnel.',
#                            code='on_save_missing_domaine_fonctionnel'
#                       )
#                    cptdeplev1 = form.cleaned_data['cptdeplev1']
#                    if not cptdeplev1:
#                        raise forms.ValidationError(
#                            "Veuillez renseigner l'enveloppe comptable.",
#                            code='on_save_missing_enveloppe_comptable'
#                       )
#                    dateae = form.cleaned_data['dateae']
#                    if not dateae:
#                        raise forms.ValidationError(
#                            'Veuillez renseigner la date de ae.',
#                            code='on_save_missing_date_ae'
#                       )
#            else:
#                print ('no clean data for this form')
#
#
#class BaseRecetteFullFormSet(BaseModelFormSet):
#
#    def clean(self):
#        if any(self.errors):
#            return
#
#        for form in self.forms:
#            if form.cleaned_data:
#                if form.cleaned_data['myid']:
#                    montantre = form.cleaned_data['montantre']
#                    if not montantre:
#                        raise forms.ValidationError(
#                            'Veuillez renseigner montantre.',
#                            code='on_save_missing_montantre'
#                        )
#
#                    montantar = form.cleaned_data['montantar']
#                    if not montantar:
#                        raise forms.ValidationError(
#                            'Veuillez renseigner montantar.',
#                            code='on_save_missing_montantar'
#                       )
#                    montantdc = form.cleaned_data['montantdc']
#                    if not montantdc:
#                        raise forms.ValidationError(
#                            'Veuillez renseigner montantdc.',
#                            code='on_save_missing_montantdc'
#                       )
#                    cptdeplev1 = form.cleaned_data['cptdeplev1']
#                    if not cptdeplev1:
#                        raise forms.ValidationError(
#                            "Veuillez renseigner l'enveloppe comptable.",
#                            code='on_save_missing_enveloppe_comptable'
#                       )
#            else:
#                print ('no clean data for this form')
