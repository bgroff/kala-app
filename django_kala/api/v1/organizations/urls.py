from django.urls import path, include

from .settings.views import *

urlpatterns = [
    path(
        'organizations/<int:organization_pk>/permission',
        name='organization_permissions',
        view=OrganizationPermissionsView.as_view()
    ),

    path(
        'organizations/<int:organization_pk>/permission/<int:pk>',
        name='organization_permission',
        view=OrganizationPermissionView.as_view()
    ),
]
