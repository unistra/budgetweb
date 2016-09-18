from django import forms
from collections import OrderedDict
from decimal import Decimal

from .models import (Depense, PlanFinancement, Recette, NatureComptableDepense)


class RecetteForm(forms.ModelForm):

    enveloppe = forms.ChoiceField(required=False, widget=forms.Select(
        attrs={'class': 'form-enveloppe'}))
    montant_dc = forms.DecimalField(
        label='DC', widget=forms.TextInput(attrs={'class': 'decimal'}))
    montant_ar = forms.DecimalField(
        label='AR', widget=forms.TextInput(attrs={'class': 'form-naturecomptablerecette decimal'}))
    montant_re = forms.DecimalField(
        label='RE', widget=forms.TextInput(attrs={'class': 'decimal'}))
    lienpiecejointe = forms.CharField(
        required=False,
        label='PJ', widget=forms.TextInput(attrs={'style': 'width:2px;'}))

    modal_fields = ('commentaire', 'lienpiecejointe')

    class Meta:
        model = Recette
        fields = ('annee', 'enveloppe', 'naturecomptablerecette',
                  'pfi', 'structure', 'periodebudget', 'montant_ar',
                  'montant_re', 'montant_dc', 'commentaire',
                  'lienpiecejointe')
        widgets = {
            'commentaire': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
            'annee': forms.TextInput(attrs={
                'style': 'width:50px;text-align:center;',
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
        self.is_dfi_member_or_admin = kwargs.pop('is_dfi_member_or_admin')
        natures = kwargs.pop('natures')
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        instance = self.instance

        # Fields initialization
        enveloppes = {n.enveloppe for n in natures.values()}
        enveloppe_choices = [('', '---------')] + sorted([
            (e, e) for e in set(enveloppes)])
        self.fields['enveloppe'].choices = enveloppe_choices
        self.fields['naturecomptablerecette'].choices = [('', '---------')]
        self.fields['naturecomptablerecette'].widget.attrs['class'] =\
            'form-naturecomptable form-naturecomptablerecette'

        # Set the initial values
        self.fields['structure'].initial = pfi.structure_id
        self.fields['pfi'].initial = pfi.pk
        self.fields['periodebudget'].initial = periodebudget.pk
        self.fields['annee'].initial = int(annee)

        if instance and instance.pk:
            nature = natures[instance.naturecomptablerecette_id]
            self.fields['enveloppe'].initial = nature.enveloppe
            self.fields['naturecomptablerecette'].choices += [
                (pk, str(n)) for pk, n in natures.items()\
                    if n.enveloppe == nature.enveloppe]
            self.fields['naturecomptablerecette'].initial = nature

    def save(self, commit=True):
        recette = super().save(commit=False)
        username = self.user.username
        if not recette.id:
            recette.creepar = username
        recette.modifiepar = username
        recette.save()
        return recette

    def clean_montant_dc(self):
        montant_dc = self.cleaned_data.get("montant_dc", None)
        if montant_dc is None:
            montant_dc = self.cleaned_data.get("montant_re")
        return montant_dc


class DepenseForm(forms.ModelForm):

    enveloppe = forms.ChoiceField(required=False, widget=forms.Select(
        attrs={'class': 'form-enveloppe'}))
    montant_dc = forms.DecimalField(
        label='DC', widget=forms.TextInput(attrs={'class': 'decimal'}))
    montant_ae = forms.DecimalField(
        label='AE', widget=forms.TextInput(attrs={'class': 'form-naturecomptabledepense decimal'}))
    montant_cp = forms.DecimalField(
        label='CP', widget=forms.TextInput(attrs={'class': 'decimal'}))
    lienpiecejointe = forms.CharField(
        required=False,
        label='PJ', widget=forms.TextInput(attrs={'style': 'width:2px;'}))

    modal_fields = ('commentaire', 'lienpiecejointe')

    class Meta:
        model = Depense
        fields = ('annee', 'enveloppe', 'naturecomptabledepense',
                  'pfi', 'structure',
                  'domainefonctionnel',
                  'periodebudget',
                  'montant_ae', 'montant_cp', 'montant_dc', 'commentaire',
                  'lienpiecejointe')
        widgets = {
            'commentaire': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
            'pfi': forms.HiddenInput(attrs={'readonly': 'readonly'}),
            'annee': forms.TextInput(attrs={
                'style': 'width:50px;text-align:center;',
                'readonly': 'readonly'
            }),
            'structure': forms.HiddenInput(attrs={'readonly': 'readonly'}),
            'periodebudget': forms.HiddenInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        pfi = kwargs.pop('pfi')
        periodebudget = kwargs.pop('periodebudget')
        annee = kwargs.pop('annee')
        self.is_dfi_member_or_admin = kwargs.pop('is_dfi_member_or_admin')
        self.natures = kwargs.pop('natures')
        self.domaines = kwargs.pop('domaines')
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        instance = self.instance
        # Fields initialization
        enveloppes = {n.enveloppe for n in self.natures.values()}
        enveloppe_choices = [('', '---------')] + sorted([
            (e, e) for e in set(enveloppes)])
        self.fields['enveloppe'].choices = enveloppe_choices
        self.fields['naturecomptabledepense'].choices = [('', '---------')]
        self.fields['naturecomptabledepense'].widget.attrs['class'] = \
            'form-naturecomptable form-naturecomptabledepense'
        self.fields['domainefonctionnel'].choices = [('', '---------')] + self.domaines

        # Set the initial values
        self.fields['structure'].initial = pfi.structure_id
        self.fields['pfi'].initial = pfi.pk
        self.fields['periodebudget'].initial = periodebudget.pk
        self.fields['annee'].initial = int(annee)

        if instance and instance.pk:
            nature = self.natures[instance.naturecomptabledepense_id]
            self.fields['enveloppe'].initial = nature.enveloppe
            self.fields['naturecomptabledepense'].choices += [
                (pk, str(n)) for pk, n in self.natures.items()\
                    if n.enveloppe == nature.enveloppe]
            self.fields['naturecomptabledepense'].initial = nature
            if not nature.is_decalage_tresorerie and\
               not self.is_dfi_member_or_admin:
                self.fields['montant_cp'].widget.attrs['readonly'] = True
            if not self.is_dfi_member_or_admin:
                self.fields['montant_dc'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = self.cleaned_data
        # Règle de gestion
        if not self.is_dfi_member_or_admin:
            # Première règle de gestion.
            if cleaned_data.get('naturecomptabledepense', None):
                if not cleaned_data['naturecomptabledepense'].is_decalage_tresorerie:
                    if cleaned_data.get('montant_ae', None) != cleaned_data.get('montant_cp', None):
                        raise forms.ValidationError("Le montant AE et CP ne peuvent pas être différent \
                               pour la nature comptable %s %s." % (
                            cleaned_data['naturecomptabledepense'].code_nature_comptable,
                            cleaned_data['naturecomptabledepense'].label_nature_comptable))

                # Deuxième règle de gestion.
                if cleaned_data['naturecomptabledepense'].is_non_budgetaire:
                    if cleaned_data['montant_ae'] != Decimal(0):
                        raise forms.ValidationError("Le montant AE ne peut être différent de 0 pour \
                               cette nature comptable.")
                    if cleaned_data['montant_cp'] != Decimal(0):
                        raise forms.ValidationError("Le montant CP ne peut être différent de 0 pour \
                               cette nature comptable.")
                # Trosième règle de gestion.
                # // Si "PI/CFG" = oui alors AE = DC et CP = 0
                if cleaned_data['naturecomptabledepense'].is_pi_cfg:
                    if cleaned_data['montant_cp'] != Decimal(0):
                        raise forms.ValidationError("Le montant CP ne peut être différent de 0 pour \
                               cette nature comptable.")
                    if cleaned_data.get('montant_ae', None) != cleaned_data.get('montant_dc', None):
                        raise forms.ValidationError("Le montant AE doit être identique au montant DC pour \
                               cette nature comptable.")
                # Réaffectation du  naturecomptabledepense
                self.fields['naturecomptabledepense'].choices = [('', '---------')] + [
                    (pk, str(n)) for pk, n in self.natures.items()\
                        if n.enveloppe == cleaned_data['enveloppe']]
                self.fields['naturecomptabledepense'].initial = cleaned_data['naturecomptabledepense']
            else:
                if cleaned_data.get('enveloppe', None):
                    cleaned_data['naturecomptabledepense'] = self.fields['naturecomptabledepense']
                    cleaned_data['naturecomptabledepense'].choices = [('', '---------')] + [
                        (pk, str(n)) for pk, n in self.natures.items()\
                            if n.enveloppe == cleaned_data['enveloppe']]

        return cleaned_data

    def save(self, commit=True):
        depense = super().save(commit=False)

        # Mise à jour des infos de base
        username = self.user.username
        if not depense.id:
            depense.creepar = username
        depense.modifiepar = username
        depense.save()
        return depense


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
