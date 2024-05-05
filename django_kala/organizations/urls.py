from django.urls import path
from .views import *

app_name='organizations'

urlpatterns = [
    path(
        '',
        view=OrganizationsView.as_view(),
        name='organizations',
    ),

    path(
        '<int:pk>/',
        view=OrganizationView.as_view(),
        name='organization',
    ),

    path(
        '<int:pk>/invite_user',
        view=InviteUserView.as_view(),
        name='invite_user',
    ),

    path(
        'new',
        view=NewOrganizationView.as_view(),
        name='new_organization',
    ),

    path(
        '<int:pk>/settings/details',
        view=DetailsView.as_view(),
        name='details'
    ),

    path(
        '<int:pk>/settings/delete',
        view=DeleteView.as_view(),
        name='delete'
    ),

    path(
        '<int:pk>/settings/manage_access',
        view=ManageAccessView.as_view(),
        name='manage_access'
    ),

]
