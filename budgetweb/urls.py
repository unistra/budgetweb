from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from .views import home
from . import views
from . import views2
from . import views3

admin.autodiscover()

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
    url(r'^accounts/login/$', 'django_cas.views.login'),
    url(r'^accounts/logout/$', 'django_cas.views.logout'),
    # Examples:
    url(r'^$', home, name='home'),
    url(r'^index2/$', views.index2),
    url(r'^index3/$', views.index3),
    url(r'^index3b/$', views.index3b),
    url(r'^index4/$', views.index4),
    url(r'^index5/$', views.index5),
# classe Authorisation
    url(r'^authorisation/new/$', views.authorisation_new, name='authorisation_new'),
    url(r'^authorisation/$', views.authorisation_list,name='authorisation_list'),
    url(r'^authorisationuser/$', views.authorisation_user,name='authorisation_user'),
    url(r'^authorisation/(?P<pkauth>[0-9]+)/detail/$', views.authorisation_detail, name='authorisation_detail'),
    url(r'^authorisation/(?P<pkauth>[0-9]+)/delete/$', views.authorisation_delete, name='authorisation_delete'),
    url(r'^authorisation/import/$', views.authorisation_importcsv,name='authorisation_importcsv'),
    url(r'^authorisation/deleteall/$', views.authorisation_deleteall, name='authorisation_deleteall'),
# classe NatureComptable
    url(r'^naturecomptable/new/$', views.naturecomptable_new, name='naturecomptable_new'),
    url(r'^naturecomptable/$', views.naturecomptable_list,name='naturecomptable_list'),
    url(r'^naturecomptable/(?P<pkcc>[0-9]+)/detail/$', views.naturecomptable_detail, name='naturecomptable_detail'),
    url(r'^naturecomptable/(?P<pkcc>[0-9]+)/delete/$', views.naturecomptable_delete, name='naturecomptable_delete'),
    url(r'^naturecomptable/(?P<pkcc>[0-9]+)/edit/$', views.naturecomptable_edit, name='naturecomptable_edit'),
    url(r'^naturecomptable/import/$', views.naturecomptable_importcsv,name='naturecomptable_importcsv'),
    url(r'^naturecomptable/deleteall/$', views.naturecomptable_deleteall, name='naturecomptable_deleteall'),
# classe DomaineFonctionnel
    url(r'^domainefonctionnel/new/$', views.domainefonctionnel_new, name='domainefonctionnel_new'),
    url(r'^domainefonctionnel/$', views.domainefonctionnel_list,name='domainefonctionnel_list'),
    url(r'^domainefonctionnel/(?P<pkdf>[0-9]+)/detail/$', views.domainefonctionnel_detail, name='domainefonctionnel_detail'),
    url(r'^domainefonctionnel/(?P<pkdf>[0-9]+)/delete/$', views.domainefonctionnel_delete, name='domainefonctionnel_delete'),
    url(r'^domainefonctionnel/import/$', views.domainefonctionnel_importcsv,name='domainefonctionnel_importcsv'),
    url(r'^domainefonctionnel/deleteall/$', views.domainefonctionnel_deleteall, name='domainefonctionnel_deleteall'),
#Compte Budgetaire
    url(r'^comptebudget/new/$', views.comptebudget_new, name='comptebudget_new'),
    url(r'^comptebudget/$', views.comptebudget_list,name='comptebudget_list'),
    url(r'^comptebudget/(?P<pkcb>[0-9]+)/delete/$', views.comptebudget_delete, name='comptebudget_delete'),
#    url(r'^comptebudget/(?P<pk>[0-9]+)/edit/$', views.comptebudget_edit, name='comptebudget_edit'),
#ComptaNature
    url(r'^comptanature/new/$', views.comptanature_new, name='comptanature_new'),
    url(r'^comptanature/$', views.comptanature_list,name='comptanature_list'),
    url(r'^comptanature/(?P<pkcb>[0-9]+)/delete/$', views.comptanature_delete, name='comptanature_delete'),
    url(r'^comptanature/(?P<pk>[0-9]+)/edit/$', views.comptanature_edit, name='comptanature_edit'),
#FondBudgetaire
    url(r'^fondbudgetaire/new/$', views.fondbudgetaire_new, name='fondbudgetaire_new'),
    url(r'^fondbudgetaire/$', views.fondbudgetaire_list,name='fondbudgetaire_list'),
    url(r'^fondbudgetaire/(?P<pkcb>[0-9]+)/delete/$', views.fondbudgetaire_delete, name='fondbudgetaire_delete'),
    url(r'^fondbudgetaire/(?P<pk>[0-9]+)/edit/$', views.fondbudgetaire_edit, name='fondbudgetaire_edit'),
# classe Structure
    url(r'^structure/new/$', views.structure_new, name='structure_new'),
    url(r'^structure/$', views.structure_list,name='structure_list'),
    url(r'^structure/list2$', views.structure_list2,name='structure_list2'),
    url(r'^structure/(?P<pkst>[0-9]+)/detail/$', views.structure_detail, name='structure_detail'),
    url(r'^structure/(?P<pkst>[0-9]+)/delete/$', views.structure_delete, name='structure_delete'),
    url(r'^structure/(?P<pkst>[0-9]+)/edit/$', views.structure_edit, name='structure_edit'),
    url(r'^structure/import/$', views.structure_importcsv,name='structure_importcsv'),
    url(r'^structure/deleteall/$', views.structure_deleteall, name='structure_deleteall'),
    url(r'^structure/set_parent/$', views.structure_set_parent, name='structure_set_parent'),
# classe PlanFinancement
    url(r'^planfinancement/new/$', views.planfinancement_new, name='planfinancement_new'),
    url(r'^planfinancement/$', views.planfinancement_list,name='planfinancement_list'),
    url(r'^planfinancementavecrecdep/$', views.liste_pfi_avec_depenses_recettes,name='liste_pfi_avec_depenses_recettes'),
    url(r'^planfinancement/(?P<pkpfi>[0-9]+)/detail/$', views.planfinancement_detail, name='planfinancement_detail'),
    url(r'^planfinancement/(?P<pkpfi>[0-9]+)/delete/$', views.planfinancement_delete, name='planfinancement_delete'),
    url(r'^planfinancement/(?P<pkpfi>[0-9]+)/edit/$', views.planfinancement_edit, name='planfinancement_edit'),
    url(r'^planfinancement/import/$', views.planfinancement_importcsv,name='planfinancement_importcsv'),
    url(r'^planfinancement/deleteall/$', views.planfinancement_deleteall, name='planfinancement_deleteall'),
# class DepenseFull
    url(r'^depensefull/new_avec_pfi_cflink/(?P<struct3id>\w+)/(?P<pfiid>[0-9]+)$', views.depensefull_new_avec_pfi_cflink, name='depensefull_new_avec_pfi_cflink'),
    url(r'^depensefull/$', views.depensefull_list,name='depensefull_list'),
    url(r'^depensefull/regroup/$', views.depensefull_listregroup,name='depensefull_listregroup'),
    url(r'^depensefull/(?P<pkdep>[0-9]+)/detail/$', views.depensefull_detail, name='depensefull_detail'),
    url(r'^depensefull/(?P<pkdep>[0-9]+)/detail2/$', views.depensefull_detail2, name='depensefull_detail2'),
    url(r'^depensefull/(?P<pkdep>[0-9]+)/delete/$', views.depensefull_delete, name='depensefull_delete'),
    url(r'^depensefull/(?P<pkdep>[0-9]+)/delete2/$', views.depensefull_delete2, name='depensefull_delete2'),
    url(r'^depensefull/(?P<pkdep>[0-9]+)/edit/$', views.depensefull_edit, name='depensefull_edit'),
    url(r'^depensefull/(?P<pkdep>[0-9]+)/edit2/$', views.depensefull_edit2, name='depensefull_edit2'),
    url(r'^depensefull/deleteall/$', views.depensefull_deleteall, name='depensefull_deleteall'),
    url(r'^depensefull/(?P<pkcc>[0-9]+)/parcc/$', views.depensefull_parcc, name='depensefull_parcc'),
    url(r'^depensefull/baseformsetdepensefullavec_pfi_cflink/(?P<struct3id>\w+)/(?P<pfiid>[0-9]+)$', views.baseformsetdepensefullavec_pfi_cflink, name='baseformsetdepensefullavec_pfi_cflink'),

# class RecetteFull
    url(r'^recettefull/new_avec_pfi_cflink/(?P<struct3id>\w+)/(?P<pfiid>[0-9]+)$', views.recettefull_new_avec_pfi_cflink, name='recettefull_new_avec_pfi_cflink'),
    url(r'^recettefull/baseformsetrecettefullavec_pfi_cflink/(?P<struct3id>\w+)/(?P<pfiid>[0-9]+)$', views.baseformsetrecettefullavec_pfi_cflink, name='baseformsetrecettefullavec_pfi_cflink'),
    url(r'^recettefull/$', views.recettefull_list,name='recettefull_list'),
    url(r'^recettefull/(?P<pkrec>[0-9]+)/detail/$', views.recettefull_detail, name='recettefull_detail'),
    url(r'^recettefull/(?P<pkrec>[0-9]+)/detail2/$', views.recettefull_detail2, name='recettefull_detail2'),
    url(r'^recettefull/(?P<pkrec>[0-9]+)/delete/$', views.recettefull_delete, name='recettefull_delete'),
    url(r'^recettefull/(?P<pkrec>[0-9]+)/delete2/$', views.recettefull_delete2, name='recettefull_delete2'),
    url(r'^recettefull/(?P<pkrec>[0-9]+)/edit/$', views.recettefull_edit, name='recettefull_edit'),
    url(r'^recettefull/(?P<pkrec>[0-9]+)/edit2/$', views.recettefull_edit2, name='recettefull_edit2'),
    url(r'^recettefull/deleteall/$', views.depensefull_deleteall, name='recettefull_deleteall'),
    url(r'^recettefull/(?P<pkcp>[0-9]+)/parcp/$', views.recettefull_parcp, name='recettefull_parcp'),

# class PeriodeBudget
    url(r'^periodebudget/new/$', views.periodebudget_new, name='periodebudget_new'),
    url(r'^periodebudget/$', views.periodebudget_list,name='periodebudget_list'),
    url(r'^periodebudget/(?P<pkpb>[0-9]+)/detail/$', views.periodebudget_detail, name='periodebudget_detail'),
    url(r'^periodebudget/(?P<pkpb>[0-9]+)/delete/$', views.periodebudget_delete, name='periodebudget_delete'),

#Ajax depenses
    url(r'^ajax/ajax_add/(?P<pkstr1>[0-9]+)/$', views.ajax_add_todo1,name="ajax_add_todo1"),
    url(r'^ajax/ajax_findstruct_lev3/(?P<pkstr1>[0-9]+)/$', views.ajax_findstruct_lev3,name="ajax_findstruct_lev3"),
    url(r'^ajax/ajax_findorigfond_lev2/(?P<pkor>[0-9]+)/$', views.ajax_findorigfond_lev2,name="ajax_findorigfond_lev2"),
    url(r'^ajax/ajax_add_cptdev_lev2/(?P<pkcpt>[0-9]+)/$', views.ajax_add_cptdev_lev2,name="ajax_add_cptdev_lev2"),
    url(r'^ajax/more/$',views.ajax_more_todo1, name ="ajax_more_todo1"),
    url(r'^ajax/ajax_add_enveloppe_depense/(?P<pkstr1>[0-9]+)/(?P<lenveloppe>\w+)/$', views.ajax_add_enveloppe_depense,name="ajax_add_enveloppe_depense"),
    url(r'^ajax/ajax_add_enveloppetype_depense/(?P<pkstr1>[0-9]+)/$', views.ajax_add_enveloppetype_depense,name="ajax_add_enveloppetype_depense"),
    url(r'^ajax/ajax_get_enveloppe_decalage/(?P<pkstr1>[0-9]+)/$', views.ajax_get_enveloppe_decalage ,name="ajax_get_enveloppe_decalage"),
# Presentation / Affichage
    url(r'^menu1/$', views2.menu_list14tree, name='menu1_list'),
    url(r'^menu2/$', views3.menu_list15tree, name='menu2_list'),
#Ajax recettes
    url(r'^ajax/ajax_recadd/(?P<pkstr1>[0-9]+)/$', views.ajax_recadd_todo1,name="ajax_recadd_todo1"),
    url(r'^ajax/ajax_recfindstruct_lev3/(?P<pkstr1>[0-9]+)/$', views.ajax_recfindstruct_lev3,name="ajax_recfindstruct_lev3"),
    url(r'^ajax/ajax_recfindorigfond_lev2/(?P<pkor>[0-9]+)/$', views.ajax_recfindorigfond_lev2,name="ajax_recfindorigfond_lev2"),
    url(r'^ajax/ajax_recadd_cptdev_lev2/(?P<pkcpt>[0-9]+)/$', views.ajax_recadd_cptdev_lev2,name="ajax_recadd_cptdev_lev2"),
    url(r'^ajax/ajax_add_enveloppe/(?P<pkstr1>[0-9]+)/(?P<lenveloppe>\w+)/$', views.ajax_add_enveloppe,name="ajax_add_enveloppe"),
    url(r'^ajax/ajax_add_enveloppetype/(?P<pkstr1>[0-9]+)/$', views.ajax_add_enveloppetype,name="ajax_add_enveloppetype"),
    url(r'^ajax/ajax_recette_displaycompte/(?P<pkstr1>[0-9]+)/$', views.ajax_recette_displaycompte ,name="ajax_recette_displaycompte"),

#AJAX GENERAL
    url(r'^ajax/ajax_add_eotp/(?P<pkstr1>[0-9]+)/$', views.ajax_add_eotp,name="ajax_add_eotp"),
    # url(r'^app/', include('apps.app.urls')),

    url(r'^admin/', include(admin.site.urls)),
]

# debug toolbar for dev
if settings.DEBUG and 'debug_toolbar'in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
