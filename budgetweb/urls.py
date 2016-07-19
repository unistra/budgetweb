from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from .views import home
from . import views

admin.autodiscover()

urlpatterns = [
    url(r'^accounts/login/$', 'django_cas.views.login'),
    url(r'^accounts/logout/$', 'django_cas.views.logout'),
    # Examples:
    url(r'^$', home, name='home'),

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
    url(r'^depense/(?P<pfiid>\w+)/(?P<annee>\w+)$',
        views.depense, name="depense"),
    url(r'^recette/(?P<pfiid>\w+)/(?P<annee>\w+)$',
        views.recette, name="recette"),

    url(r'^admin/', include(admin.site.urls)),

]
# debug toolbar for dev
if settings.DEBUG and 'debug_toolbar'in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
