from django.conf import settings
from django.conf.urls import url, include
from django.views.defaults import page_not_found, permission_denied, server_error

from .views import Home, SearchView, LicenseView, UserDocumentationView


urlpatterns = [
    url(
        regex=r'^$',
        view=Home.as_view(),
        name='home'
    ),

    url(
        regex=r'^search/$',
        view=SearchView.as_view(),
        name='search'
    ),

    url(
        r'^',
        include('api.basecamp_classic.urls'),
    ),

    url(
        r'^v1/',
        include('api.v1.urls'),
    ),

    url(
        r'^organizations/',
        include('organizations.urls'),
    ),

    url(
        r'^accounts/',
        include('auth.urls'),
    ),

    url(
        r'^projects/',
        include('projects.urls'),
    ),

    url(
        regex=r'^license$',
        view=LicenseView.as_view(),
        name='license',
    ),

    url(
        regex=r'^user_documentation$',
        view=UserDocumentationView.as_view(),
        name='user_documentation',
    ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^404/$', page_not_found, {'exception': Exception()}),
        url(r'^403/$', permission_denied, {'exception': Exception()}),
        url(r'^500/$', server_error, ),

    ] + urlpatterns
