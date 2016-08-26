# -*- coding: utf-8 -*-

"""
"""

from collections import OrderedDict
from functools import reduce

from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import (Depense, DomaineFonctionnel, NatureComptableDepense,
                     NatureComptableRecette, PeriodeBudget, PlanFinancement,
                     Recette, Structure, StructureAuthorizations)


class DepenseAdmin(admin.ModelAdmin):
    list_display = ('pfi', 'structure', 'domainefonctionnel',
                    'naturecomptabledepense', 'periodebudget', 'annee',
                    'montant_ae', 'montant_cp', 'montant_dc')
    search_fields = ['pfi', 'structure', 'domainefonctionnel',
                     'naturecomptabledepense', 'periodebudget', 'annee']
admin.site.register(Depense, DepenseAdmin)


class DomaineFonctionnelAdmin(admin.ModelAdmin):
    list_display = ('code', 'label_court', 'label')
    search_fields = ['code', 'label_court', 'label']
admin.site.register(DomaineFonctionnel, DomaineFonctionnelAdmin)


class NatureComptableDepenseAdmin(admin.ModelAdmin):
    field = ('is_fleche', 'enveloppe', 'label_nature_comptable',
             'code_nature_comptable', 'code_compte_budgetaire',
             'label_compte_budgetaire',
             'is_decalage_tresorerie', 'is_active')
    list_display = ('is_fleche', 'enveloppe', 'label_nature_comptable',
                    'code_nature_comptable', 'code_compte_budgetaire',
                    'label_compte_budgetaire',
                    'is_decalage_tresorerie', 'is_active')
    search_fields = ['enveloppe', 'label_nature_comptable',
                     'code_nature_comptable', 'code_compte_budgetaire',
                     'label_compte_budgetaire', 'is_fleche',
                     'is_decalage_tresorerie', 'is_active']

    class Meta:
        ordering = ['is_fleche', 'enveloppe']
admin.site.register(NatureComptableDepense, NatureComptableDepenseAdmin)


class NatureComptableRecetteAdmin(admin.ModelAdmin):
    field = ('is_fleche', 'enveloppe', 'code_fonds', 'label_fonds',
             'code_nature_comptable', 'label_nature_comptable',
             'code_compte_budgetaire', 'label_compte_budgetaire',
             'is_active')
    list_display = ('is_fleche', 'enveloppe', 'code_fonds', 'label_fonds',
                    'code_nature_comptable', 'label_nature_comptable',
                    'code_compte_budgetaire', 'label_compte_budgetaire',
                    'is_active')
    search_fields = ['is_fleche', 'enveloppe', 'code_fonds', 'label_fonds',
                     'code_nature_comptable', 'label_nature_comptable',
                     'code_compte_budgetaire', 'label_compte_budgetaire',
                     'is_active']

    class Meta:
        ordering = ['is_fleche', 'enveloppe']
admin.site.register(NatureComptableRecette, NatureComptableRecetteAdmin)


class PeriodeBudgetAdmin(admin.ModelAdmin):
    field = ('code', 'label', 'annee', 'is_active')
    list_display = ('code', 'label', 'annee', 'is_active')
    search_fields = ['code', 'label', 'annee', 'is_active']
admin.site.register(PeriodeBudget, PeriodeBudgetAdmin)


class PlanFinancementAdmin(admin.ModelAdmin):
    field = ('structure', 'code', 'label', 'eotp', 'centrecoutderive',
             'centreprofitderive', 'is_fleche', 'is_pluriannuel', 'is_active',
             'date_debut', 'date_fin')
    list_display = ('structure', 'code', 'label', 'eotp', 'centrecoutderive',
                    'centreprofitderive', 'is_fleche', 'is_pluriannuel',
                    'is_active', 'date_debut', 'date_fin')
    search_fields = ['structure', 'code', 'eotp', 'centrecoutderive',
                     'centreprofitderive', 'is_fleche', 'is_pluriannuel',
                     'is_active', 'date_debut', 'date_fin']

    class Meta:
        ordering = ['is_fleche', 'structure']
admin.site.register(PlanFinancement, PlanFinancementAdmin)


class RecetteAdmin(admin.ModelAdmin):
    list_display = ('pfi', 'structure',
                    'naturecomptablerecette', 'periodebudget', 'annee',
                    'montant_ar', 'montant_re', 'montant_dc')
    search_fields = ['pfi', 'structure', 'naturecomptablerecette',
                     'periodebudget', 'annee']
admin.site.register(Recette, RecetteAdmin)


class StructureAdmin(admin.ModelAdmin):
    field = ('code', 'parent', 'type', 'label', 'is_active')
    list_display = ('code', 'parent', 'type', 'label', 'is_active')
    search_fields = ['type', 'code', 'label']

    class Meta:
        ordering = ['is_active', 'code']
admin.site.register(Structure, StructureAdmin)


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
