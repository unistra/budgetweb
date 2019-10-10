# -*- coding: utf-8 -*-

"""
"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import (DomaineFonctionnel, NatureComptableDepense,
                     NatureComptableRecette, PlanFinancement, Structure)


class DomaineFonctionnelAdmin(admin.ModelAdmin):
    list_display = ('code', 'label_court', 'label')
    search_fields = ['code', 'label_court', 'label']


admin.site.register(DomaineFonctionnel, DomaineFonctionnelAdmin)


class NatureComptableDepenseAdmin(admin.ModelAdmin):
    fields = ('is_fleche', 'enveloppe', 'label_nature_comptable',
              'code_nature_comptable', 'code_compte_budgetaire',
              'label_compte_budgetaire', 'is_decalage_tresorerie',
              'is_non_budgetaire', 'is_pi_cfg', 'is_active')
    list_display = ('get_str', 'is_active', 'is_fleche', 'enveloppe',
                    'label_compte_budgetaire', 'is_decalage_tresorerie',
                    'is_non_budgetaire', 'is_pi_cfg')
    search_fields = ['enveloppe', 'label_nature_comptable',
                     'code_nature_comptable', 'code_compte_budgetaire',
                     'label_compte_budgetaire', 'is_fleche', 'is_active']

    def get_str(self, obj):
        return '{0} ({1.code_compte_budgetaire})'.format(str(obj), obj)
    get_str.short_description = _('accounting nature')


admin.site.register(NatureComptableDepense, NatureComptableDepenseAdmin)


class NatureComptableRecetteAdmin(admin.ModelAdmin):
    fields = ('is_fleche', 'enveloppe', 'code_fonds', 'label_fonds',
              'code_nature_comptable', 'label_nature_comptable',
              'code_compte_budgetaire', 'label_compte_budgetaire',
              'is_ar_and_re', 'is_non_budgetaire', 'is_active')
    list_display = ('get_str', 'is_fleche', 'enveloppe', 'code_fonds',
                    'label_fonds', 'label_compte_budgetaire', 'is_ar_and_re',
                    'is_non_budgetaire', 'is_active')
    search_fields = ['is_fleche', 'enveloppe', 'code_fonds', 'label_fonds',
                     'code_nature_comptable', 'label_nature_comptable',
                     'code_compte_budgetaire', 'label_compte_budgetaire',
                     'is_active']

    def get_str(self, obj):
        return '{0} ({1.code_compte_budgetaire})'.format(str(obj), obj)
    get_str.short_description = _('accounting nature')


admin.site.register(NatureComptableRecette, NatureComptableRecetteAdmin)


class PlanFinancementAdmin(admin.ModelAdmin):
    fields = ('structure', 'code', 'label', 'eotp', 'centrecoutderive',
              'centreprofitderive', 'groupe1', 'groupe2', 'is_fleche',
              'is_pluriannuel', 'is_active', 'date_debut', 'date_fin')
    list_display = ('get_str', 'label', 'eotp', 'centrecoutderive',
                    'centreprofitderive', 'is_fleche', 'is_pluriannuel',
                    'is_active', 'date_debut', 'date_fin', 'groupe1',
                    'groupe2')
    search_fields = ['structure__code', 'code', 'eotp', 'centrecoutderive',
                     'centreprofitderive', 'is_fleche', 'is_pluriannuel',
                     'is_active', 'date_debut', 'date_fin', 'groupe1',
                     'groupe2']

    def get_str(self, obj):
        return str(obj)
    get_str.short_description = _('structure')

    class Meta:
        ordering = ['pk', 'is_fleche', 'structure']


admin.site.register(PlanFinancement, PlanFinancementAdmin)


class StructureAdmin(admin.ModelAdmin):
    fields = ('code', 'parent', 'groupe1', 'groupe2', 'label', 'is_active')
    list_display = ('code', 'parent', 'groupe1', 'groupe2', 'label',
                    'is_active')
    search_fields = ['code', 'label', 'groupe1', 'groupe2']

    class Meta:
        ordering = ['is_active', 'code']


admin.site.register(Structure, StructureAdmin)
