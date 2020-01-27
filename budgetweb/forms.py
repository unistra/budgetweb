from decimal import Decimal

from django import forms
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from budgetweb.apps.structure.models import PlanFinancement
from .models import Depense, Recette


class RecetteForm(forms.ModelForm):

    enveloppe = forms.ChoiceField(required=False, widget=forms.Select(
        attrs={'class': 'form-enveloppe'}))
    montant_dc = forms.DecimalField(
        label='Produits / Ressources',
        widget=forms.TextInput(
            attrs={'class': 'form-naturecomptablerecette decimal'}))
    montant_ar = forms.DecimalField(
        label='AR', widget=forms.TextInput(
            attrs={'class': 'form-naturecomptablerecette decimal'}))
    montant_re = forms.DecimalField(
        label='RE', widget=forms.TextInput(
            attrs={'class': 'form-naturecomptablerecette decimal'}))
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
        self.is_dfi = kwargs.pop('is_dfi')
        self.natures = kwargs.pop('natures')
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        instance = self.instance

        # Fields initialization
        enveloppes = {n.enveloppe for n in self.natures.values()}
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
            nature = self.natures.get(instance.naturecomptablerecette_id)
            if nature:
                self.fields['enveloppe'].initial = nature.enveloppe
                self.fields['naturecomptablerecette'].choices += [
                    (pk, str(n)) for pk, n in self.natures.items()
                    if n.enveloppe == nature.enveloppe]
                self.fields['naturecomptablerecette'].initial = nature

                if nature.is_ar_and_re and not self.is_dfi:
                    self.fields['montant_re'].widget.attrs['readonly'] = True
                if nature.is_non_budgetaire and not self.is_dfi:
                    self.fields['montant_ar'].widget.attrs['readonly'] = True
                    self.fields['montant_re'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = self.cleaned_data
        nature = cleaned_data.get('naturecomptablerecette', None)
        # Règle de gestion
        if not self.is_dfi:
            # Première règle de gestion.
            if nature:
                # * Si "AR et RE" = oui  alors AR = RE
                if nature.is_ar_and_re:
                    if cleaned_data.get('montant_ar', None) != cleaned_data.get('montant_re', None):
                        raise forms.ValidationError("Le montant AR et RE ne peuvent pas être différent \
                               pour la nature comptable %s %s." % (
                            nature.code_nature_comptable,
                            nature.label_nature_comptable))

                # Si "non budgétaire (dont PI)" = oui alors AR = RE = 0 et DC à saisir
                if nature.is_non_budgetaire:
                    if cleaned_data['montant_ar'] != Decimal(0):
                        raise forms.ValidationError("Le montant AR ne peut être différent de 0 pour \
                               cette nature comptable.")
                    if cleaned_data['montant_re'] != Decimal(0):
                        raise forms.ValidationError("Le montant RE ne peut être différent de 0 pour \
                               cette nature comptable.")
                # Réaffectation du  naturecomptabledepense
                self.fields['naturecomptablerecette'].choices = [('', '---------')] + [
                    (pk, str(n)) for pk, n in self.natures.items()
                    if n.enveloppe == cleaned_data['enveloppe']]
                self.fields['naturecomptablerecette'].initial = nature
            else:
                if cleaned_data.get('enveloppe', None):
                    cleaned_data['naturecomptablerecette'] = self.fields['naturecomptablerecette']
                    cleaned_data['naturecomptablerecette'].choices = [('', '---------')] + [
                        (pk, str(n)) for pk, n in self.natures.items()
                        if n.enveloppe == cleaned_data['enveloppe']]
        else:
            if nature:
                self.fields['naturecomptablerecette'].choices = [('', '---------')] + [
                    (pk, str(n)) for pk, n in self.natures.items()
                    if n.enveloppe == cleaned_data['enveloppe']]
                self.fields['naturecomptablerecette'].initial = nature
            else:
                if cleaned_data.get('enveloppe', None):
                    cleaned_data['naturecomptablerecette'] = self.fields['naturecomptablerecette']
                    cleaned_data['naturecomptablerecette'].choices = [('', '---------')] + [
                        (pk, str(n)) for pk, n in self.natures.items()
                        if n.enveloppe == cleaned_data['enveloppe']]
        return cleaned_data

    def save(self, commit=True):
        recette = super().save(commit=False)
        username = self.user.username
        if not recette.id:
            recette.creepar = username
        recette.modifiepar = username
        recette.save()
        return recette


class DepenseForm(forms.ModelForm):

    enveloppe = forms.ChoiceField(required=False, widget=forms.Select(
        attrs={'class': 'form-enveloppe'}))
    montant_dc = forms.DecimalField(
        label='Charges / Immos',
        widget=forms.TextInput(
            attrs={'class': 'form-naturecomptabledepense decimal'}))
    montant_ae = forms.DecimalField(
        label='AE', widget=forms.TextInput(
            attrs={'class': 'form-naturecomptabledepense decimal'}))
    montant_cp = forms.DecimalField(
        label='CP', widget=forms.TextInput(
            attrs={'class': 'form-naturecomptabledepense decimal'}))
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
        self.is_dfi = kwargs.pop('is_dfi')
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
            nature = self.natures.get(instance.naturecomptabledepense_id)
            if nature:
                self.fields['enveloppe'].initial = nature.enveloppe
                self.fields['naturecomptabledepense'].choices += [
                    (pk, str(n)) for pk, n in self.natures.items()\
                        if n.enveloppe == nature.enveloppe]
                self.fields['naturecomptabledepense'].initial = nature
                if not nature.is_decalage_tresorerie and not self.is_dfi:
                    self.fields['montant_cp'].widget.attrs['readonly'] = True
                if not self.is_dfi:
                    self.fields['montant_dc'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = self.cleaned_data
        nature = cleaned_data.get('naturecomptabledepense', None)
        # Règle de gestion
        if not self.is_dfi:
            # Première règle de gestion.
            if nature:
                if nature.is_decalage_tresorerie:
                    if cleaned_data.get('montant_cp', None) != cleaned_data.get('montant_dc', None):
                        raise forms.ValidationError("Le montant CP et DC ne peuvent pas être différent pour la nature comptable %s %s." % (
                            nature.code_nature_comptable,
                            nature.label_nature_comptable))

                # Deuxième règle de gestion.
                if nature.is_non_budgetaire:
                    if cleaned_data['montant_ae'] != Decimal(0):
                        raise forms.ValidationError("Le montant AE ne peut être différent de 0 pour cette nature comptable.")
                    if cleaned_data['montant_cp'] != Decimal(0):
                        raise forms.ValidationError("Le montant CP ne peut être différent de 0 pour cette nature comptable.")
                # Trosième règle de gestion.
                # // Si "PI/CFG" = oui alors AE = DC et CP = 0
                if nature.is_pi_cfg:
                    if cleaned_data['montant_cp'] != Decimal(0):
                        raise forms.ValidationError("Le montant CP ne peut être différent de 0 pour cette nature comptable.")
                    if cleaned_data.get('montant_ae', None) != cleaned_data.get('montant_dc', None):
                        raise forms.ValidationError("Le montant AE doit être identique au montant DC pour \
                               cette nature comptable.")

                # Règle par défaut
                if not nature.is_decalage_tresorerie and\
                   not nature.is_non_budgetaire and\
                   not nature.is_pi_cfg:
                    if cleaned_data.get('montant_ae', None) != cleaned_data.get('montant_cp', None):
                        raise forms.ValidationError("Le montant AE et CP ne peuvent pas être différent \
                              pour la nature comptable %s %s." % (
                           nature.code_nature_comptable,
                           nature.label_nature_comptable))
                    if cleaned_data.get('montant_cp', None) != cleaned_data.get('montant_dc', None):
                        raise forms.ValidationError("Le montant CP et DC ne peuvent pas être différent \
                               pour la nature comptable %s %s." % (
                            nature.code_nature_comptable,
                            nature.label_nature_comptable))
                # Réaffectation du  naturecomptabledepense
                self.fields['naturecomptabledepense'].choices = [('', '---------')] + [
                    (pk, str(n)) for pk, n in self.natures.items()\
                        if n.enveloppe == cleaned_data['enveloppe']]
                self.fields['naturecomptabledepense'].initial = nature
            else:
                if cleaned_data.get('enveloppe', None):
                    cleaned_data['naturecomptabledepense'] = self.fields['naturecomptabledepense']
                    cleaned_data['naturecomptabledepense'].choices = [('', '---------')] + [
                        (pk, str(n)) for pk, n in self.natures.items()\
                            if n.enveloppe == cleaned_data['enveloppe']]
        else:
            if nature:
                self.fields['naturecomptabledepense'].choices = [('', '---------')] + [
                    (pk, str(n)) for pk, n in self.natures.items()\
                        if n.enveloppe == cleaned_data['enveloppe']]
                self.fields['naturecomptabledepense'].initial = nature
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
        instance = self.instance
        cleaned_data = self.cleaned_data
        date_debut = cleaned_data.get("date_debut")
        date_fin = cleaned_data.get("date_fin")

        if date_fin and date_debut:
            if date_fin < date_debut:
                cleaned_data.pop('date_debut')
                cleaned_data.pop('date_fin')
                raise forms.ValidationError(
                    "La date de début est inférieure à la date de fin !")

            # Check if the are existing accountings which are not in the new
            # period
            has_compta = any(
                model.objects.filter(
                    Q(pfi=instance.pk),
                    Q(annee__lt=date_debut.year) | Q(annee__gt=date_fin.year)
                ).exists() for model in (Depense, Recette))

            if has_compta:
                cleaned_data.pop('date_debut')
                cleaned_data.pop('date_fin')
                raise forms.ValidationError(
                    _('There are already entries which are not in the new period'))

        return cleaned_data
