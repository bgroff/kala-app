from django.urls import path
from .views import *

app_name = 'projects'

urlpatterns = [
    path(
        '',
        view=ProjectsView.as_view(),
        name='projects'
    ),

    path(
        'new_project',
        view=NewProjectView.as_view(),
        name='new_project'
    ),

    path(
        '<int:pk>/',
        view=ProjectView.as_view(),
        name='project'
    ),

    path(
        '<int:pk>/invite_user',
        view=ProjectInviteUserView.as_view(),
        name='project_invite_user'
    ),

    path(
        '<int:pk>/download',
        view=ExportProjectView.as_view(),
        name='export_project'
    ),

    path(
        '<int:project_pk>/new_document',
        view=NewDocumentView.as_view(),
        name='new_document'
    ),

    path(
        '<int:project_pk>/<int:document_pk>',
        view=DocumentView.as_view(),
        name='document'
    ),

    path(
        '<int:project_pk>/<int:document_pk>/download',
        view=ExportDocumentView.as_view(),
        name='export_document'
    ),

    path(
        '<int:project_pk>/<int:document_pk>/new_version',
        view=NewDocumentVersionView.as_view(),
        name='new_version'
    ),

    path(
        '<int:project_pk>/<int:document_pk>/<uuid:version_uuid>/download',
        view=DocumentDownload.as_view(),
        name='download'
    ),

    path(
        '<int:project_pk>/<int:document_pk>/invite_user',
        view=DocumentInviteUserView.as_view(),
        name='document_invite_user'
    ),

    path(
        '<int:project_pk>/<int:document_pk>/settings/details',
        view=DocumentDetailsView.as_view(),
        name='document_details'
    ),

    # url(
    #     regex=r'^(?P<project_pk>\d+)/(?P<document_pk>\d+)/settings/archive',
    #     view=DocumentArchiveView.as_view(),
    #     name='document_archive'
    # ),

    path(
        '<int:project_pk>/<int:document_pk>/settings/delete',
        view=DocumentDeleteView.as_view(),
        name='document_delete'
    ),

    path(
        '<int:project_pk>/<int:document_pk>/settings/manage_access',
        view=DocumentManageAccessView.as_view(),
        name='document_manage_access'
    ),

    path(
        '<int:project_pk>/<int:document_pk>/settings/transfer_ownership',
        view=DocumentTransferOwnershipView.as_view(),
        name='document_transfer_ownership'
    ),

    path(
        '<int:pk>/settings/details',
        view=DetailsView.as_view(),
        name='details'
    ),

    # url(
    #     regex=r'^(?P<pk>\d+)/settings/archive$',
    #     view=ArchiveView.as_view(),
    #     name='archive'
    # ),

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

    path(
        '<int:pk>/settings/transfer_ownership',
        view=TransferOwnershipView.as_view(),
        name='transfer_ownership'
    ),

    path(
        '<int:pk>/settings/categories',
        view=CategoriesView.as_view(),
        name='categories'
    ),

    path(
        '<int:pk>/settings/categories/<int:category_pk>',
        view=CategoriesView.as_view(),
        name='delete_category'
    ),

    path(
        '<int:pk>/settings/new_category',
        view=NewCategoryView.as_view(),
        name='new_category'
    ),

    path(
        '<int:project_pk>/settings/<int:category_pk>/edit_category',
        view=EditCategoryView.as_view(),
        name='edit_category'
    ),
]
