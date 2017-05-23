# -*- coding: utf-8 -*-

"""
"""

from collections import OrderedDict
from functools import reduce

from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _

from budgetweb.apps.structure.models import Structure
from .models import (Depense, PeriodeBudget, Recette, StructureAuthorizations,
                     StructureMontant, Virement)


def deactivate_periods(modeladmin, request, queryset):
    queryset.update(is_active=False)
deactivate_periods.short_description = _("Mark selected periods as deactivated")


def activate_periods(modeladmin, request, queryset):
    queryset.update(is_active=True)
activate_periods.short_description = _("Mark selected periods as activated")


class DepenseAdmin(admin.ModelAdmin):
    list_display = ('pfi', 'structure', 'domainefonctionnel',
                    'naturecomptabledepense', 'periodebudget', 'annee',
                    'montant_ae', 'montant_cp', 'montant_dc')
    search_fields = ['pfi', 'structure', 'domainefonctionnel',
                     'naturecomptabledepense', 'periodebudget', 'annee']
admin.site.register(Depense, DepenseAdmin)


class PeriodeBudgetAdmin(admin.ModelAdmin):
    list_display = ('period_code', 'annee', 'is_active',
                    'date_debut_saisie', 'date_fin_saisie',
                    'date_debut_retardataire', 'date_fin_retardataire',
                    'date_debut_dfi', 'date_fin_dfi',
                    'date_debut_admin', 'date_fin_admin')
    search_fields = ['period__code', 'annee', 'is_active']
    ordering = ['annee', 'period__order']
    actions = [deactivate_periods, activate_periods]

    def period_code(self, obj):
        return obj.period.code


admin.site.register(PeriodeBudget, PeriodeBudgetAdmin)


class RecetteAdmin(admin.ModelAdmin):
    list_display = ('pfi', 'structure',
                    'naturecomptablerecette', 'periodebudget', 'annee',
                    'montant_ar', 'montant_re', 'montant_dc')
    search_fields = ['pfi', 'structure', 'naturecomptablerecette',
                     'periodebudget', 'annee']
admin.site.register(Recette, RecetteAdmin)


class StructureMontantAdmin(admin.ModelAdmin):
    list_display = ('structure', 'periodebudget', 'annee',
                    'depense_montant_dc', 'depense_montant_cp',
                    'depense_montant_ae', 'recette_montant_dc',
                    'recette_montant_ar', 'recette_montant_re')
    search_fields = ['structure', 'periodebudget__period__code', 'annee']
admin.site.register(StructureMontant, StructureMontantAdmin)


class VirementAdmin(admin.ModelAdmin):
    fields = ('document_number', 'document_type', 'version', 'perimetre',
             'process')
    list_display = ('document_number', 'document_type', 'version',
                    'perimetre', 'process')
    search_fields = ['document_number', 'depense__structure__code']

    class Meta:
        ordering = ['document_number']
admin.site.register(Virement, VirementAdmin)


class StructureAuthorizationsForm(forms.ModelForm):
    structures = forms.MultipleChoiceField(
        widget=FilteredSelectMultiple(
            verbose_name='User field permissions',
            is_stacked=False,
        ),
        help_text='Structures autorisées pour cet utilisateur. Ajouter un '
                  'utilisateur à une structure lui donnera automatiquement '
                  'accès à toutes ses structures filles.'
    )

    class Meta:
        model = StructureAuthorizations
        exclude = []

    def structures_tree(self, nodes):
        """
        Return the structures choices.
        """
        def get_from_dict(data_dict, map_list):
            """get from nested dict"""
            return reduce(lambda d, k: d[k][1], map_list, data_dict)

        def tree_nodes(node_tree, i=0):
            """get the tree nodes as a tuple"""
            result = []
            for node_id, node in node_tree.items():
                result.append((node_id, '%s%s%s'\
                    % ('--' * i, ' ' if i else '', node[0])))
                result.extend(tree_nodes(node[1], i + 1))
            return result

        # Build the structures dict
        dict_tree = OrderedDict()
        for node in nodes:
            pc = node.parent.pk if node.parent else ''
            p = list(map(int, node.path.split('/')[1:-1]))
            if not pc:
                dict_tree[node.pk] = (node.code, OrderedDict())
            else:
                f = get_from_dict(dict_tree, p)
                f[pc][1].setdefault(node.pk, (node.code, OrderedDict()))

        # Transform the structures dict into a list
        result = tree_nodes(dict_tree)
        return result

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        nodes = Structure.objects.all().select_related('parent').order_by('depth', 'code')
        self.fields['structures'].choices = self.structures_tree(nodes)


class StructureAuthorizationsAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
    form = StructureAuthorizationsForm

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        structures = form.instance.structures.all()
        for structure in structures:
            for child in structure.get_children():
                form.instance.structures.add(child)

admin.site.register(StructureAuthorizations, StructureAuthorizationsAdmin)
