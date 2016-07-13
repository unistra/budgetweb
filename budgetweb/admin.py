# -*- coding: utf-8 -*-

"""
"""

from django.contrib import admin

from .models import (Depense, DomaineFonctionnel, NatureComptableDepense,
                     NatureComptableRecette, PeriodeBudget, PlanFinancement,
                     Recette, Structure)


class DepenseAdmin(admin.ModelAdmin):
    pass
admin.site.register(Depense, DepenseAdmin)


class DomaineFonctionnelAdmin(admin.ModelAdmin):
    pass
admin.site.register(DomaineFonctionnel, DomaineFonctionnelAdmin)


class NatureComptableDepenseAdmin(admin.ModelAdmin):
    pass
admin.site.register(NatureComptableDepense, NatureComptableDepenseAdmin)


class NatureComptableRecetteAdmin(admin.ModelAdmin):
    pass
admin.site.register(NatureComptableRecette, NatureComptableRecetteAdmin)


class PeriodeBudgetAdmin(admin.ModelAdmin):
    pass
admin.site.register(PeriodeBudget, PeriodeBudgetAdmin)


class PlanFinancementAdmin(admin.ModelAdmin):
    pass
admin.site.register(PlanFinancement, PlanFinancementAdmin)


class RecetteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Recette, RecetteAdmin)


class StructureAdmin(admin.ModelAdmin):
    pass
admin.site.register(Structure, StructureAdmin)
