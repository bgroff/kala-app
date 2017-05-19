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

   # url(
   #     regex=r'^(?P<pk>\d+)/permissions/$',
   #     view=ProjectPermissions.as_view(),
   #     name='permissions'
   # ),

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
