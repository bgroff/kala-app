from django.urls import path, include

from api.v1.projects.settings.views import DocumentPermissionsView, DocumentPermissionView, ProjectPermissionsView, ProjectPermissionView
from .views import *

urlpatterns = [
    path(
        'projects/',
        name='projects',
        view=ProjectsView.as_view()
    ),

    path(
        'projects/<int:pk>/',
        name='project',
        view=ProjectView.as_view()
    ),

    path(
        'projects/<int:pk>/documents/',
        name='documents',
        view=DocumentsView.as_view()
    ),

    path(
        'projects/<int:project_pk>/documents/<int:document_pk>/',
        name='document',
        view=DocumentView.as_view()
    ),

    path(
        'projects/<int:project_pk>/permission',
        name='document',
        view=ProjectPermissionsView.as_view()
    ),

    path(
        'projects/<int:project_pk>/permission/<int:pk>',
        name='document',
        view=ProjectPermissionView.as_view()
    ),

    path(
        'projects/<int:project_pk>/documents/<int:document_pk>/permission',
        name='document',
        view=DocumentPermissionsView.as_view()
    ),

    path(
        'projects/<int:project_pk>/documents/<int:document_pk>/permission/<int:pk>',
        name='document',
        view=DocumentPermissionView.as_view()
    ),

]
