from django.conf.urls import url
from .views import *

app_name='projects'

urlpatterns = [
    url(
        regex=r'^$',
        view=ProjectsView.as_view(),
        name='projects'
    ),

    url(
        regex=r'^new_project$',
        view=NewProjectView.as_view(),
        name='new_project'
    ),

    url(
        regex=r'^(?P<pk>\d+)/$',
        view=ProjectView.as_view(),
        name='project'
    ),

    url(
        regex=r'^(?P<pk>\d+)/invite_user$',
        view=ProjectInviteUserView.as_view(),
        name='project_invite_user'
    ),

    url(
        regex=r'^(?P<pk>\d+)/download$',
        view=ExportProjectView.as_view(),
        name='export_project'
    ),

    url(
        regex=r'^(?P<project_pk>\d+)/new_document$',
        view=NewDocumentView.as_view(),
        name='new_document'
    ),

    url(
        regex=r'^(?P<project_pk>\d+)/(?P<document_pk>\d+)$',
        view=DocumentView.as_view(),
        name='document'
    ),

    url(
        regex=r'^(?P<project_pk>\d+)/(?P<document_pk>\d+)/download$',
        view=ExportDocumentView.as_view(),
        name='export_document'
    ),

    url(
        regex=r'^(?P<project_pk>\d+)/(?P<document_pk>\d+)/new_version$',
        view=NewDocumentVersionView.as_view(),
        name='new_version'
    ),

    url(
        regex=r'^(?P<project_pk>\d+)/(?P<document_pk>\d+)/(?P<version_uuid>[a-f0-9]{8}-?[a-f0-9]{4}-?[1-5][a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/download$',
        view=DocumentDownload.as_view(),
        name='download'
    ),

    url(
        regex=r'^(?P<project_pk>\d+)/(?P<document_pk>\d+)/invite_user$',
        view=DocumentInviteUserView.as_view(),
        name='document_invite_user'
    ),

    url(
        regex=r'^(?P<project_pk>\d+)/(?P<document_pk>\d+)/settings/details$',
        view=DocumentDetailsView.as_view(),
        name='document_details'
    ),


    url(
        regex=r'^(?P<project_pk>\d+)/(?P<document_pk>\d+)/settings/archive',
        view=DocumentArchiveView.as_view(),
        name='document_archive'
    ),


    url(
        regex=r'^(?P<project_pk>\d+)/(?P<document_pk>\d+)/settings/manage_access$',
        view=DocumentManageAccessView.as_view(),
        name='document_manage_access'
    ),

    url(
        regex=r'^(?P<pk>\d+)/settings/details$',
        view=DetailsView.as_view(),
        name='details'
    ),

    url(
        regex=r'^(?P<pk>\d+)/settings/archive$',
        view=ArchiveView.as_view(),
        name='archive'
    ),

    url(
        regex=r'^(?P<pk>\d+)/settings/manage_access$',
        view=ManageAccessView.as_view(),
        name='manage_access'
    ),

    url(
        regex=r'^(?P<pk>\d+)/settings/transfer_ownership$',
        view=TransferOwnershipView.as_view(),
        name='transfer_ownership'
    ),

    url(
        regex=r'^(?P<pk>\d+)/settings/categories$',
        view=CategoriesView.as_view(),
        name='categories'
    ),

    url(
        regex=r'^(?P<pk>\d+)/settings/categories/(?P<category_pk>\d+)$',
        view=CategoriesView.as_view(),
        name='delete_category'
    ),

    url(
        regex=r'^(?P<pk>\d+)/settings/new_category$',
        view=NewCategoryView.as_view(),
        name='new_category'
    ),

    url(
        regex=r'^(?P<project_pk>\d+)/settings/(?P<category_pk>\d+)/edit_category$',
        view=EditCategoryView.as_view(),
        name='edit_category'
    ),
]
