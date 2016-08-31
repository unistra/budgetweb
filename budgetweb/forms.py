from django import forms

from .models import (Depense, PlanFinancement, Recette)


class RecetteForm(forms.ModelForm):

    enveloppe = forms.ChoiceField(required=False, widget=forms.Select(
        attrs={'class': 'form-enveloppe'}))
    montant_dc = forms.DecimalField(
        label='DC', widget=forms.TextInput(attrs={'style': 'width:90px;'}))
    montant_ar = forms.DecimalField(
        label='AR', widget=forms.TextInput(attrs={'style': 'width:90px;'}))
    montant_re = forms.DecimalField(
        label='RE', widget=forms.TextInput(attrs={'style': 'width:90px;'}))
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
        is_dfi_member_or_admin = kwargs.pop('is_dfi_member_or_admin')
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
            'form-naturecomptable'

        # Set the initial values
        self.fields['structure'].initial = pfi.structure_id
        self.fields['pfi'].initial = pfi.pk
        self.fields['periodebudget'].initial = periodebudget.pk
        self.fields['annee'].initial = int(annee)

        # Règle de gestion, le champ DC n'est autorisé que pour la DFI.
        if not is_dfi_member_or_admin:
            self.fields['montant_dc'].widget.attrs['readonly'] = True
            self.fields['montant_dc'].required = False

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
        label='DC', widget=forms.TextInput(attrs={'style': 'width:90px;'}))
    montant_ae = forms.DecimalField(
        label='AE', widget=forms.TextInput(attrs={'style': 'width:90px;',
                                                  'class': 'form-naturecomptabledepense'}))
    montant_cp = forms.DecimalField(
        label='CP', widget=forms.TextInput(attrs={'style': 'width:90px;',
                                                  'class': 'form-naturecomptabledepense'}))
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
        is_dfi_member_or_admin = kwargs.pop('is_dfi_member_or_admin')
        natures = kwargs.pop('natures')
        domaines = kwargs.pop('domaines')
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        instance = self.instance

        # Fields initialization
        enveloppes = {n.enveloppe for n in natures.values()}
        enveloppe_choices = [('', '---------')] + sorted([
            (e, e) for e in set(enveloppes)])
        self.fields['enveloppe'].choices = enveloppe_choices
        self.fields['naturecomptabledepense'].choices = [('', '---------')]
        self.fields['naturecomptabledepense'].widget.attrs['class'] = \
            'form-naturecomptable form-naturecomptabledepense'
        self.fields['domainefonctionnel'].choices = domaines

        # Set the initial values
        self.fields['structure'].initial = pfi.structure_id
        self.fields['pfi'].initial = pfi.pk
        self.fields['periodebudget'].initial = periodebudget.pk
        self.fields['annee'].initial = int(annee)

        # Règle de gestion, le champ DC n'est autorisé que pour la DFI.
        if not is_dfi_member_or_admin:
            self.fields['montant_dc'].widget.attrs['readonly'] = True
            self.fields['montant_dc'].required = False

        if instance and instance.pk:
            nature = natures[instance.naturecomptabledepense_id]
            self.fields['enveloppe'].initial = nature.enveloppe
            self.fields['naturecomptabledepense'].choices += [
                (pk, str(n)) for pk, n in natures.items()\
                    if n.enveloppe == nature.enveloppe]
            self.fields['naturecomptabledepense'].initial = nature
            if not nature.is_decalage_tresorerie:
                self.fields['montant_cp'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        depense = super().save(commit=False)
        username = self.user.username
        if not depense.id:
            depense.creepar = username
        depense.modifiepar = username
        depense.save()
        return depense

    def clean_montant_dc(self):
        montant_dc = self.cleaned_data.get("montant_dc", None)
        if montant_dc is None:
            montant_dc = self.cleaned_data.get("montant_cp")
        return montant_dc


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
