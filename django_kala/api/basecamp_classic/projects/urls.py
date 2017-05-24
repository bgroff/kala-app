from django.conf.urls import url
from .views import *

urlpatterns = [
   url(
       regex=r'^projects.xml$',
       view=ProjectsView.as_view(),
       name='projects'
   ),

   url(
       regex=r'^projects/(?P<pk>\d+).xml$',
       view=ProjectView.as_view(),
       name='company'
   ),

   url(
       regex=r'^projects/(?P<pk>\d+)/people.xml$',
       view=PeopleView.as_view(),
       name='people'
   ),

   url(
       regex=r'^projects/(?P<pk>\d+)/categories.xml$',
       view=CategoriesView.as_view(),
       name='categories'
   ),

   url(
       regex=r'^projects/(?P<pk>\d+)/attachments.xml$',
       view=DocumentsView.as_view(),
       name='documents'
   ),
]
