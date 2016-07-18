from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from .views import home
from . import views

admin.autodiscover()

urlpatterns = [
#    url(r'^search/$', views.search, name='search'),
    url(r'^accounts/login/$', 'django_cas.views.login'),
    url(r'^accounts/logout/$', 'django_cas.views.logout'),
    # Examples:
    url(r'^$', home, name='home'),
## classe Authorisation
#    url(r'^authorisation/new/$', views.authorisation_new, name='authorisation_new'),
    url(r'^authorisation/$', views.authorisation_list,name='authorisation_list'),
#    url(r'^authorisationuser/$', views.authorisation_user,name='authorisation_user'),
#    url(r'^authorisation/(?P<pkauth>[0-9]+)/detail/$', views.authorisation_detail, name='authorisation_detail'),
#    url(r'^authorisation/(?P<pkauth>[0-9]+)/delete/$', views.authorisation_delete, name='authorisation_delete'),
#    url(r'^authorisation/import/$', views.authorisation_importcsv,name='authorisation_importcsv'),
#    url(r'^authorisation/deleteall/$', views.authorisation_deleteall, name='authorisation_deleteall'),

## classe PlanFinancement
#    url(r'^planfinancement/new/$', views.planfinancement_new, name='planfinancement_new'),
#    url(r'^planfinancement/$', views.planfinancement_list,name='planfinancement_list'),
#    url(r'^planfinancement/(?P<pkpfi>[0-9]+)/detail/$', views.planfinancement_detail, name='planfinancement_detail'),
#    url(r'^planfinancement/(?P<pkpfi>[0-9]+)/delete/$', views.planfinancement_delete, name='planfinancement_delete'),
#    url(r'^planfinancement/(?P<pkpfi>[0-9]+)/edit/$', views.planfinancement_edit, name='planfinancement_edit'),
#    url(r'^planfinancement/import/$', views.planfinancement_importcsv,name='planfinancement_importcsv'),
#    url(r'^planfinancement/deleteall/$', views.planfinancement_deleteall, name='planfinancement_deleteall'),

##Ajax depenses
#    url(r'^ajax/ajax_add/(?P<pkstr1>[0-9]+)/$', views.ajax_add_todo1,name="ajax_add_todo1"),
#    url(r'^ajax/ajax_findstruct_lev3/(?P<pkstr1>[0-9]+)/$', views.ajax_findstruct_lev3,name="ajax_findstruct_lev3"),
#    url(r'^ajax/ajax_findorigfond_lev2/(?P<pkor>[0-9]+)/$', views.ajax_findorigfond_lev2,name="ajax_findorigfond_lev2"),
#    url(r'^ajax/ajax_add_cptdev_lev2/(?P<pkcpt>[0-9]+)/$', views.ajax_add_cptdev_lev2,name="ajax_add_cptdev_lev2"),
#    url(r'^ajax/more/$',views.ajax_more_todo1, name ="ajax_more_todo1"),
#    url(r'^ajax/ajax_add_enveloppe_depense/(?P<pkstr1>[0-9]+)/(?P<lenveloppe>\w+)/$', views.ajax_add_enveloppe_depense,name="ajax_add_enveloppe_depense"),
#    url(r'^ajax/ajax_add_enveloppetype_depense/(?P<pkstr1>[0-9]+)/$', views.ajax_add_enveloppetype_depense,name="ajax_add_enveloppetype_depense"),
#    url(r'^ajax/ajax_get_enveloppe_decalage/(?P<pkstr1>[0-9]+)/$', views.ajax_get_enveloppe_decalage ,name="ajax_get_enveloppe_decalage"),
##Ajax recettes
#    url(r'^ajax/ajax_recadd/(?P<pkstr1>[0-9]+)/$', views.ajax_recadd_todo1,name="ajax_recadd_todo1"),
#    url(r'^ajax/ajax_recfindstruct_lev3/(?P<pkstr1>[0-9]+)/$', views.ajax_recfindstruct_lev3,name="ajax_recfindstruct_lev3"),
#    url(r'^ajax/ajax_recfindorigfond_lev2/(?P<pkor>[0-9]+)/$', views.ajax_recfindorigfond_lev2,name="ajax_recfindorigfond_lev2"),
#    url(r'^ajax/ajax_recadd_cptdev_lev2/(?P<pkcpt>[0-9]+)/$', views.ajax_recadd_cptdev_lev2,name="ajax_recadd_cptdev_lev2"),
#    url(r'^ajax/ajax_add_enveloppe/(?P<pkstr1>[0-9]+)/(?P<lenveloppe>\w+)/$', views.ajax_add_enveloppe,name="ajax_add_enveloppe"),
#    url(r'^ajax/ajax_add_enveloppetype/(?P<pkstr1>[0-9]+)/$', views.ajax_add_enveloppetype,name="ajax_add_enveloppetype"),
#    url(r'^ajax/ajax_recette_displaycompte/(?P<pkstr1>[0-9]+)/$', views.ajax_recette_displaycompte ,name="ajax_recette_displaycompte"),

    # Base de l'arbre.
    url(r'^showtree/(?P<type_affichage>\w+)/$', views.show_tree,
        name="show_tree"),
    # Affichage AJAX.
    url(r'^showtree/(?P<type_affichage>\w+)/getsubtree/(?P<structid>\w+)$',
        views.show_sub_tree, name="show_sub_tree"),
    # Pluriannuel
    url(r'^pluriannuel/(?P<pfiid>\w+)$', views.pluriannuel,
        name="pluriannuel"),
    # Détails d'un PFI
    url(r'^detailspfi/(?P<pfiid>\w+)$', views.detailspfi,
        name="detailspfi"),
    url(r'^depense/(?P<pfiid>\w+)/', views.depense, name="depense"),
    url(r'^recette/(?P<pfiid>\w+)/', views.recette, name="recette"),

    url(r'^admin/', include(admin.site.urls)),

]
# debug toolbar for dev
if settings.DEBUG and 'debug_toolbar'in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
