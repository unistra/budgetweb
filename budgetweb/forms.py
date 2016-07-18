from django import forms
from django.forms.formsets import BaseFormSet
from django.forms.models import modelformset_factory, BaseModelFormSet
from django.http import Http404, HttpResponse

from .models import (Authorisation, Depense, DomaineFonctionnel,
                     NatureComptableDepense, NatureComptableRecette,
                     PeriodeBudget, PlanFinancement, Recette, Structure)


# class AuthorisationForm(forms.ModelForm):
#
#    class Meta:
#        model = Authorisation
#        fields = ('username', 'myobject')


class BaseRecetteFormSet(BaseFormSet):
    def clean(self):
        pass


class RecetteForm(forms.ModelForm):

    montant_dc = forms.DecimalField(widget=forms.NumberInput(
                     attrs={'style': 'width:100px;',
                            'step': ''}))
    montant_ar = montant_re = montant_dc

    class Meta:
        model = Recette
        fields = ('pfi', 'structure', 'periodebudget',
                  'naturecomptablerecette', 'annee',
                  'montant_ar', 'montant_re', 'montant_dc', 'commentaire',
                  'lienpiecejointe')
        widgets = {
            'commentaire': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
            'annee': forms.NumberInput(attrs={
                        'style': 'width:50px;-moz-appearance: textfield;',
                        'class': 'toto'}),
            'pfi': forms.HiddenInput(),
            'structure': forms.HiddenInput(),
            'periodebudget': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        pfi = kwargs.pop('pfi')
        periodebudget = kwargs.pop('periodebudget')
        super(RecetteForm, self).__init__(*args, **kwargs)
        is_fleche = pfi.is_fleche
        structure = pfi.structure
        nc = NatureComptableRecette.objects.filter(is_fleche=is_fleche)
        self.fields['naturecomptablerecette'].queryset = nc
        self.fields['structure'].initial = structure.pk
        self.fields['structure'].widget.attrs['readonly'] = True
        self.fields['pfi'].initial = pfi.pk
        self.fields['pfi'].widget.attrs['readonly'] = True
        self.fields['periodebudget'].initial = periodebudget.pk
        self.fields['periodebudget'].widget.attrs['readonly'] = True
        self.fields['annee'].widget.attrs['readonly'] = True
        self.fields['annee'].initial = 2017


class DepenseForm(forms.ModelForm):

    montant_dc = forms.DecimalField(label='Montant DC',
                                    widget=forms.NumberInput(
                                     attrs={'style': 'width:100px;',
                                            'step': ''}))
    montant_ae = forms.DecimalField(label='Montant AE',
                                    widget=forms.NumberInput(
                                     attrs={'style': 'width:100px;',
                                            'step': ''}))
    montant_cp = forms.DecimalField(label='Montant CP',
                                    widget=forms.NumberInput(
                                     attrs={'style': 'width:100px;',
                                            'step': ''}))

    class Meta:
        model = Depense
        fields = ('pfi', 'structure', 'domainefonctionnel',
                  'periodebudget', 'naturecomptabledepense', 'annee',
                  'montant_ae', 'montant_cp', 'montant_dc', 'commentaire',
                  'lienpiecejointe')
        widgets = {
            'commentaire': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
            'pfi': forms.HiddenInput(),
            'annee': forms.NumberInput(attrs={
                        'style': 'width:50px;-moz-appearance: textfield;',
                        'class': 'toto'}),
            'structure': forms.HiddenInput(),
            'periodebudget': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        pfi = kwargs.pop('pfi')
        periodebudget = kwargs.pop('periodebudget')
        super(DepenseForm, self).__init__(*args, **kwargs)
        is_fleche = pfi.is_fleche
        structure = pfi.structure
        nc = NatureComptableDepense.objects.filter(is_fleche=is_fleche)
        self.fields['naturecomptabledepense'].queryset = nc
        self.fields['structure'].initial = structure.pk
        self.fields['structure'].widget.attrs['readonly'] = True
        self.fields['pfi'].initial = pfi.pk
        self.fields['pfi'].widget.attrs['readonly'] = True
        self.fields['periodebudget'].initial = periodebudget.pk
        self.fields['periodebudget'].widget.attrs['readonly'] = True
        self.fields['annee'].widget.attrs['readonly'] = True
        self.fields['annee'].initial = 2017


class PlanFinancementPluriForm(forms.ModelForm):

    date_debut = forms.DateField(required=False, widget=forms.DateInput(
                                 attrs={'class': 'datetimepicker'}))
    date_fin = forms.DateField(required=False, widget=forms.DateInput(
                               attrs={'class': 'datetimepicker'}))

    class Meta:
        model = PlanFinancement
        fields = ('date_debut', 'date_fin')

    def clean(self):
        super(PlanFinancementPluriForm, self).clean()
        date_debut = self.cleaned_data.get("date_debut")
        date_fin = self.cleaned_data.get("date_fin")

        if date_fin and date_debut and date_fin < date_debut:
            raise forms.ValidationError(
                "La date de début est inférieur à la date de fin !")
