from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from .views import home
from . import views

admin.autodiscover()

urlpatterns = [
    url(r'^accounts/login/$', 'django_cas.views.login'),
    url(r'^accounts/logout/$', 'django_cas.views.logout'),
    url(r'^$', home, name='home'),

    # Ajax
    url(r'^api/(?P<model>naturecomptablerecette|naturecomptabledepense)/enveloppe/(?P<enveloppe>\w+)/(?P<pfiid>\w+)/$',
        views.api_fund_designation_by_nature_and_enveloppe,
        name='api-fund-designation-by-nature-and-enveloppe'),

    url(r'^api/(?P<model>naturecomptablerecette|naturecomptabledepense)/(?P<id_nature>\w+)/$',
        views.api_get_details_nature_by_code,
        name='api_get_details_nature_by_code'),
    url(r'^api/naturecomptabledepense/is_decalage_tresorerie/(?P<id_naturecomptabledepense>\w+)/$',
        views.api_get_decalage_tresorerie_by_id,
        name='api_get_decalage_tresorerie_by_id'),

    # Base de l'arbre.
    url(r'^showtree/(?P<type_affichage>\w+)/(?P<structid>\w+)/$',
        views.show_tree, name="show_tree_structid"),
    url(r'^showtree/(?P<type_affichage>\w+)/$', views.show_tree,
        name="show_tree"),

    # Pluriannuel
    url(r'^pluriannuel/(?P<pfiid>\w+)/$', views.pluriannuel,
        name="pluriannuel"),

    # Détails d'un PFI
    url(r'^detailspfi/(?P<pfiid>\w+)/$', views.detailspfi,
        name="detailspfi"),
    url(r'^detailscf/(?P<structid>\w+)/$', views.detailscf,
        name="detailscf"),
    url(r'^depense/(?P<pfiid>\w+)/(?P<annee>\w+)/$',
        views.depense, name="depense"),
    url(r'^recette/(?P<pfiid>\w+)/(?P<annee>\w+)/$',
        views.recette, name="recette"),

    url(r'^admin/', include(admin.site.urls)),

]
# debug toolbar for dev
if settings.DEBUG and 'debug_toolbar'in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
