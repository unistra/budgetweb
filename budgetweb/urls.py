from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.i18n import JavaScriptCatalog

from . import get_version
from . import views

admin.autodiscover()
admin.site.site_header = f'Budgetweb v.{get_version()}'

handler500 = 'budgetweb.views.handler500'

urlpatterns = [
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('accounts/', include('django_cas.urls', namespace='django_cas')),

    path('', views.home, name='home'),

    # Ajax
    # TODO: move to budgetweb.libs.api
    re_path(r'^api/(?P<model>naturecomptablerecette|naturecomptabledepense)/enveloppe/(?P<enveloppe>\w+)/(?P<pfiid>\w+)/$',
            views.api_fund_designation_by_nature_and_enveloppe,
            name='api-fund-designation-by-nature-and-enveloppe'),
    re_path(r'^api/(?P<model>naturecomptablerecette|naturecomptabledepense)/(?P<id_nature>\w+)/$',
            views.api_get_details_nature_by_code,
            name='api_get_details_nature_by_code'),
    path('api/naturecomptabledepense/rules/<int:id_naturecomptabledepense>/',
         views.api_get_managment_rules_depense_by_id,
         name='api_get_managment_rules_depense_by_id'),
    path('api/naturecomptablerecette/rules/<int:id_naturecomptablerecette>/',
         views.api_get_managment_rules_recette_by_id,
         name='api_get_managment_rules_recette_by_id'),
    path('api/updateMontantDC/', views.api_set_dcfield_value_by_id,
         name='api_set_dcfield_value_by_id'),

    # Base de l'arbre.
    path('showtree/<str:type_affichage>/<int:structid>/',
         views.show_tree, name="show_tree_structid"),
    path('showtree/<str:type_affichage>/', views.show_tree, name="show_tree"),

    # Pluriannuel
    path('pluriannuel/<int:pfiid>/', views.pluriannuel, name="pluriannuel"),

    # Détails d'un PFI
    path('detailspfi/<int:pfiid>/', views.detailspfi, name="detailspfi"),
    path('detailscf/<int:structid>/', views.detailscf, name="detailscf"),
    path('depense/<int:pfiid>/<int:annee>/', views.depense, name="depense"),
    path('recette/<int:pfiid>/<int:annee>/', views.recette, name="recette"),

    path('setyear/', views.set_year, name='set_year'),

    # Administration
    path('admin/', admin.site.urls),
    path('migrate_pluriannuel/<int:period_id>/',
         views.migrate_pluriannuel, name='migrate-pluriannuel'),
]

# debug toolbar for dev
if settings.DEBUG and 'debug_toolbar'in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
