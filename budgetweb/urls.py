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
# classe CompteComptable
    url(r'^comptecomptable/new/$', views.comptecomptable_new, name='comptecomptable_new'),
    url(r'^comptecomptable/$', views.comptecomptable_list,name='comptecomptable_list'),
    url(r'^comptecomptable/(?P<pkcc>[0-9]+)/detail/$', views.comptecomptable_detail, name='comptecomptable_detail'),
    url(r'^comptecomptable/(?P<pkcc>[0-9]+)/delete/$', views.comptecomptable_delete, name='comptecomptable_delete'),
    url(r'^comptecomptable/import/$', views.comptecomptable_importcsv,name='comptecomptable_importcsv'),
    url(r'^comptecomptable/deleteall/$', views.comptecomptable_deleteall, name='comptecomptable_deleteall'),
# classe DomaineFonctionnel
    url(r'^domainefonctionnel/new/$', views.domainefonctionnel_new, name='domainefonctionnel_new'),
    url(r'^domainefonctionnel/$', views.domainefonctionnel_list,name='domainefonctionnel_list'),
    url(r'^domainefonctionnel/(?P<pkdf>[0-9]+)/detail/$', views.domainefonctionnel_detail, name='domainefonctionnel_detail'),
    url(r'^domainefonctionnel/(?P<pkdf>[0-9]+)/delete/$', views.domainefonctionnel_delete, name='domainefonctionnel_delete'),
    url(r'^domainefonctionnel/import/$', views.domainefonctionnel_importcsv,name='domainefonctionnel_importcsv'),
    url(r'^domainefonctionnel/deleteall/$', views.domainefonctionnel_deleteall, name='domainefonctionnel_deleteall'),
# classe OrigineFonds
    url(r'^originefonds/new/$', views.originefonds_new, name='originefonds_new'),
    url(r'^originefonds/$', views.originefonds_list,name='originefonds_list'),
    url(r'^originefonds/(?P<pkof>[0-9]+)/detail/$', views.originefonds_detail, name='originefonds_detail'),
    url(r'^originefonds/(?P<pkof>[0-9]+)/delete/$', views.originefonds_delete, name='originefonds_delete'),
    url(r'^originefonds/import/$', views.originefonds_importcsv,name='originefonds_importcsv'),
    url(r'^originefonds/deleteall/$', views.originefonds_deleteall, name='originefonds_deleteall'),
# classe Structure
    url(r'^structure/new/$', views.structure_new, name='structure_new'),
    url(r'^structure/$', views.structure_list,name='structure_list'),
    url(r'^structure/(?P<pkst>[0-9]+)/detail/$', views.structure_detail, name='structure_detail'),
    url(r'^structure/(?P<pkst>[0-9]+)/delete/$', views.structure_delete, name='structure_delete'),
    url(r'^structure/import/$', views.structure_importcsv,name='structure_importcsv'),
    url(r'^structure/deleteall/$', views.structure_deleteall, name='structure_deleteall'),
# classe PlanFinancement
    url(r'^planfinancement/new/$', views.planfinancement_new, name='planfinancement_new'),
    url(r'^planfinancement/$', views.planfinancement_list,name='planfinancement_list'),
    url(r'^planfinancement/(?P<pkpfi>[0-9]+)/detail/$', views.planfinancement_detail, name='planfinancement_detail'),
    url(r'^planfinancement/(?P<pkpfi>[0-9]+)/delete/$', views.planfinancement_delete, name='planfinancement_delete'),
    url(r'^planfinancement/import/$', views.planfinancement_importcsv,name='planfinancement_importcsv'),
    url(r'^planfinancement/deleteall/$', views.planfinancement_deleteall, name='planfinancement_deleteall'),
# classe Depense
    url(r'^depense/new/$', views.depense_new, name='depense_new'),
    url(r'^depense/$', views.depense_list,name='depense_list'),
    url(r'^depense/(?P<pkdep>[0-9]+)/detail/$', views.depense_detail, name='depense_detail'),
    url(r'^depense/(?P<pkdep>[0-9]+)/delete/$', views.depense_delete, name='depense_delete'),
    url(r'^depense/import/$', views.depense_importcsv,name='depense_importcsv'),
    url(r'^depense/deleteall/$', views.depense_deleteall, name='depense_deleteall'),
# class DepenseFull
    url(r'^depensefull/new/$', views.depensefull_new, name='depensefull_new'),
    url(r'^depensefull/new2/$', views.depensefull_new2, name='depensefull_new2'),
    url(r'^depensefull/$', views.depensefull_list,name='depensefull_list'),
    url(r'^depensefull/regroup/$', views.depensefull_listregroup,name='depensefull_listregroup'),
    url(r'^depensefull/(?P<pkdep>[0-9]+)/detail/$', views.depensefull_detail, name='depensefull_detail'),
    url(r'^depensefull/(?P<pkdep>[0-9]+)/detail2/$', views.depensefull_detail2, name='depensefull_detail2'),
    url(r'^depensefull/(?P<pkdep>[0-9]+)/delete/$', views.depensefull_delete, name='depensefull_delete'),
    url(r'^depensefull/(?P<pkdep>[0-9]+)/delete2/$', views.depensefull_delete2, name='depensefull_delete2'),
    url(r'^depensefull/(?P<pkdep>[0-9]+)/edit/$', views.depensefull_edit, name='depensefull_edit'),
    url(r'^depensefull/deleteall/$', views.depensefull_deleteall, name='depensefull_deleteall'),
    url(r'^depensefull/(?P<pkcc>[0-9]+)/parcc/$', views.depensefull_parcc, name='depensefull_parcc'),
# class RecetteFull
    url(r'^recettefull/new/$', views.recettefull_new, name='recettefull_new'),
    url(r'^recettefull/new2/$', views.recettefull_new2, name='recettefull_new2'),
    url(r'^recettefull/new3/$', views.recettefull_new3, name='recettefull_new3'),
    url(r'^recettefull/$', views.recettefull_list,name='recettefull_list'),
    url(r'^recettefull/(?P<pkrec>[0-9]+)/detail/$', views.recettefull_detail, name='recettefull_detail'),
    url(r'^recettefull/(?P<pkrec>[0-9]+)/detail2/$', views.recettefull_detail2, name='recettefull_detail2'),
    url(r'^recettefull/(?P<pkrec>[0-9]+)/delete/$', views.recettefull_delete, name='recettefull_delete'),
    url(r'^recettefull/(?P<pkrec>[0-9]+)/delete2/$', views.recettefull_delete2, name='recettefull_delete2'),
    url(r'^recettefull/(?P<pkrec>[0-9]+)/edit/$', views.recettefull_edit, name='recettefull_edit'),
    url(r'^recettefull/deleteall/$', views.depensefull_deleteall, name='recettefull_deleteall'),
    url(r'^recettefull/(?P<pkcp>[0-9]+)/parcp/$', views.recettefull_parcp, name='recettefull_parcp'),
# class PeriodeBudget
    url(r'^periodebudget/new/$', views.periodebudget_new, name='periodebudget_new'),
    url(r'^periodebudget/$', views.periodebudget_list,name='periodebudget_list'),
    url(r'^periodebudget/(?P<pkpb>[0-9]+)/detail/$', views.periodebudget_detail, name='periodebudget_detail'),
    url(r'^periodebudget/(?P<pkpb>[0-9]+)/delete/$', views.periodebudget_delete, name='periodebudget_delete'),

#classe Depense essais de selections
    url(r'^depense/new2/$', views.depense_new2, name='depense_new2'),
#Ajax depenses
    url(r'^ajax/ajax_add/(?P<pkstr1>[0-9]+)/$', views.ajax_add_todo1,name="ajax_add_todo1"),
    url(r'^ajax/ajax_findstruct_lev3/(?P<pkstr1>[0-9]+)/$', views.ajax_findstruct_lev3,name="ajax_findstruct_lev3"),
    url(r'^ajax/ajax_findorigfond_lev2/(?P<pkor>[0-9]+)/$', views.ajax_findorigfond_lev2,name="ajax_findorigfond_lev2"),
    url(r'^ajax/ajax_add_cptdev_lev2/(?P<pkcpt>[0-9]+)/$', views.ajax_add_cptdev_lev2,name="ajax_add_cptdev_lev2"),
    url(r'^ajax/more/$',views.ajax_more_todo1, name ="ajax_more_todo1"),
# Presentation / Affichage
    url(r'^menu1/$', views2.menu_list14tree, name='menu1_list'),
    url(r'^menu2/$', views3.menu_list15tree, name='menu2_list'),
#Ajax recettes
    url(r'^ajax/ajax_recadd/(?P<pkstr1>[0-9]+)/$', views.ajax_recadd_todo1,name="ajax_recadd_todo1"),
    url(r'^ajax/ajax_recfindstruct_lev3/(?P<pkstr1>[0-9]+)/$', views.ajax_recfindstruct_lev3,name="ajax_recfindstruct_lev3"),
    url(r'^ajax/ajax_recfindorigfond_lev2/(?P<pkor>[0-9]+)/$', views.ajax_recfindorigfond_lev2,name="ajax_recfindorigfond_lev2"),
    url(r'^ajax/ajax_recadd_cptdev_lev2/(?P<pkcpt>[0-9]+)/$', views.ajax_recadd_cptdev_lev2,name="ajax_recadd_cptdev_lev2"),


    # url(r'^app/', include('apps.app.urls')),

    url(r'^admin/', include(admin.site.urls)),
]

# debug toolbar for dev
if settings.DEBUG and 'debug_toolbar'in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
