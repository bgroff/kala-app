from django.conf.urls import url
from .views import *

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
       regex=r'^(?P<project_pk>\d+)/(?P<document_pk>\d+)/new_version$',
       view=NewDocumentVersionView.as_view(),
       name='new_version'
   ),

   url(
       regex=r'^(?P<project_pk>\d+)/(?P<document_pk>\d+)/settings/details$',
       view=DocumentDetailsView.as_view(),
       name='document_details'
   ),

   url(
       regex=r'^(?P<pk>\d+)/settings/details$',
       view=DetailsView.as_view(),
       name='details'
   ),

   url(
       regex=r'^(?P<pk>\d+)/settings/archive',
       view=ArchiveView.as_view(),
       name='archive'
   ),

   url(
       regex=r'^(?P<pk>\d+)/settings/manage_access',
       view=ManageAccessView.as_view(),
       name='manage_access'
   ),

   url(
       regex=r'^(?P<pk>\d+)/settings/transfer_ownership$',
       view=TransferOwnershipView.as_view(),
       name='transfer_ownership'
   ),
]
