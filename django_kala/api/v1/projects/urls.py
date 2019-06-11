from django.urls import path, include

from api.v1.projects.settings.views import DocumentPermissionsView
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
        'projects/<int:project_pk>/documents/<int:document_pk>/permission',
        name='document',
        view=DocumentPermissionsView.as_view()
    ),

    # path(
    #     'projects/<int:pk>/permissions/',
    #     name='project_permissions',
    #     view=ProjectPermissionsView.as_view()
    # ),
    #
    # path(
    #     'projects/<int:project_pk>/documents/<int:document_pk>/settings',
    #     include([
    #         path('archive'),
    #         path('access'),
    #         path('ownership'),
    #     ]),
    # ),
    #
    # path(
    #     'projects/<int:pk>/settings/',
    #     include([
    #         path('archive'),
    #         path('categories'),
    #         path('access'),
    #         path('ownership'),
    #     ]),
    # ),

]
