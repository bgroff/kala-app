from django.conf import settings
from django.urls import path, include
from django.views.defaults import page_not_found, permission_denied, server_error

from .views import Home, SearchView, LicenseView, UserDocumentationView


urlpatterns = [
    path(
        '',
        view=Home.as_view(),
        name='home'
    ),

    path(
        'search/',
        view=SearchView.as_view(),
        name='search'
    ),

    path(
        'api/classic',
        include('api.basecamp_classic.urls'),
    ),

    path(
        'v1/',
        include('api.v1.urls'),
    ),

    path(
        'organizations/',
        include('organizations.urls'),
    ),

    path(
        'accounts/',
        include('auth.urls'),
    ),

    path(
        'projects/',
        include('projects.urls'),
    ),

    path(
        'license',
        view=LicenseView.as_view(),
        name='license',
    ),

    path(
        'user_documentation',
        view=UserDocumentationView.as_view(),
        name='user_documentation',
    ),
]

if settings.DEBUG:
    # import debug_toolbar
    urlpatterns = [
        # url(r'^__debug__/', include(debug_toolbar.urls)),
        path('404/', page_not_found, {'exception': Exception()}),
        path('403/', permission_denied, {'exception': Exception()}),
        path('500/', server_error, ),

    ] + urlpatterns
