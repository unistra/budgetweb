from django import forms
from django.forms.formsets import BaseFormSet, DELETION_FIELD_NAME
from django.forms.models import modelformset_factory, BaseModelFormSet
from django.http import Http404, HttpResponse

from .models import (Depense, NatureComptableDepense, NatureComptableRecette,
                     PlanFinancement, Recette)


class RecetteForm(forms.ModelForm):

    enveloppe = forms.ChoiceField(required=False, widget=forms.Select(
        attrs={'class': 'form-enveloppe'}))
    montant_dc = forms.DecimalField(
        label='DC', widget=forms.TextInput(attrs={'style': 'width:90px;'}))
    montant_ar = forms.DecimalField(
        label='AR', widget=forms.TextInput(attrs={'style': 'width:90px;'}))
    montant_re = forms.DecimalField(
        label='RE', widget=forms.TextInput(attrs={'style': 'width:90px;'}))
    lienpiecejointe = forms.CharField(required=False,
        label='PJ', widget=forms.TextInput(attrs={'style': 'width:2px;'}))

    modal_fields = ('commentaire', 'lienpiecejointe')

    class Meta:
        model = Recette
        fields = ('pfi', 'structure', 'periodebudget',
                  'annee', 'enveloppe', 'naturecomptablerecette', 'montant_ar',
                  'montant_re', 'montant_dc', 'commentaire',
                  'lienpiecejointe')
        widgets = {
            'commentaire': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
            'annee': forms.TextInput(attrs={
                'style': 'width:50px;',
                'readonly': 'readonly'
            }),
            'pfi': forms.HiddenInput(attrs={'readonly': 'readonly'}),
            'structure': forms.HiddenInput(attrs={'readonly': 'readonly'}),
            'periodebudget': forms.HiddenInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        pfi = kwargs.pop('pfi')
        periodebudget = kwargs.pop('periodebudget')
        annee = kwargs.pop('annee')
        super().__init__(*args, **kwargs)

        instance = self.instance
        is_fleche = pfi.is_fleche
        structure = pfi.structure
        natures = NatureComptableRecette.active.filter(is_fleche=is_fleche)

        # Fields initialization
        enveloppes = natures.values_list('enveloppe', flat=True)
        enveloppe_choices = [('', '---------')] + sorted([
            (e, e) for e in set(enveloppes)])
        self.fields['enveloppe'].choices = enveloppe_choices
        self.fields['naturecomptablerecette'].choices = [('', '---------')]
        self.fields['naturecomptablerecette'].queryset = natures

        # Set the initial values
        self.fields['structure'].initial = structure.pk
        self.fields['pfi'].initial = pfi.pk
        self.fields['periodebudget'].initial = periodebudget.pk
        self.fields['annee'].initial = int(annee)

        if instance and instance.pk:
            nature = instance.naturecomptablerecette
            self.fields['enveloppe'].initial = nature.enveloppe
            natures = NatureComptableRecette.active.filter(
                is_fleche=is_fleche, enveloppe=nature.enveloppe)
            self.fields['naturecomptablerecette'].choices += [
                (n.pk, str(n)) for n in natures]
            self.fields['naturecomptablerecette'].initial = nature


class DepenseForm(forms.ModelForm):

    enveloppe = forms.ChoiceField(required=False, widget=forms.Select(
        attrs={'class': 'form-enveloppe'}))
    montant_dc = forms.DecimalField(
        label='DC', widget=forms.TextInput(attrs={'style': 'width:90px;'}))
    montant_ae = forms.DecimalField(
        label='AE', widget=forms.TextInput(attrs={'style': 'width:90px;'}))
    montant_cp = forms.DecimalField(
        label='CP', widget=forms.TextInput(attrs={'style': 'width:90px;'}))
    lienpiecejointe = forms.CharField(required=False,
        label='PJ', widget=forms.TextInput(attrs={'style': 'width:2px;'}))

    modal_fields = ('commentaire', 'lienpiecejointe')

    class Meta:
        model = Depense
        fields = ('pfi', 'structure', 'domainefonctionnel', 'annee',
                  'periodebudget', 'enveloppe', 'naturecomptabledepense',
                  'montant_ae', 'montant_cp', 'montant_dc', 'commentaire',
                  'lienpiecejointe')
        widgets = {
            'commentaire': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
            'pfi': forms.HiddenInput(attrs={'readonly': 'readonly'}),
            'annee': forms.TextInput(attrs={
                'style': 'width:50px;',
                'readonly': 'readonly'
            }),
            'structure': forms.HiddenInput(attrs={'readonly': 'readonly'}),
            'periodebudget': forms.HiddenInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        pfi = kwargs.pop('pfi')
        periodebudget = kwargs.pop('periodebudget')
        annee = kwargs.pop('annee')
        super().__init__(*args, **kwargs)

        instance = self.instance
        is_fleche = pfi.is_fleche
        structure = pfi.structure
        natures = NatureComptableDepense.objects.filter(is_fleche=is_fleche)

        # Fields initialization
        enveloppes = natures.values_list('enveloppe', flat=True)
        enveloppe_choices = [('', '---------')] + sorted([
            (e, e) for e in set(enveloppes)])
        self.fields['enveloppe'].choices = enveloppe_choices
        self.fields['naturecomptabledepense'].choices = [('', '---------')]
        self.fields['naturecomptabledepense'].queryset = natures

        # Set the initial values
        self.fields['structure'].initial = structure.pk
        self.fields['pfi'].initial = pfi.pk
        self.fields['periodebudget'].initial = periodebudget.pk
        self.fields['annee'].initial = int(annee)

        if instance and instance.pk:
            nature = instance.naturecomptabledepense
            self.fields['enveloppe'].initial = nature.enveloppe
            natures = NatureComptableDepense.active.filter(
                is_fleche=is_fleche, enveloppe=nature.enveloppe)
            self.fields['naturecomptabledepense'].choices += [
                (n.pk, str(n)) for n in natures]
            self.fields['naturecomptabledepense'].initial = nature


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
                "La date de début est inférieure à la date de fin !")
