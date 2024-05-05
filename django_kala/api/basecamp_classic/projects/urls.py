from django.urls import path
from .views import *

urlpatterns = [
   path(
       'projects.xml',
       view=ProjectsView.as_view(),
       name='projects'
   ),

   path(
       'projects/<int:pk>.xml',
       view=ProjectView.as_view(),
       name='company'
   ),

   path(
       'projects/<int:pk>/people.xml',
       view=PeopleView.as_view(),
       name='people'
   ),

   path(
       'projects/<int:pk>/categories.xml',
       view=CategoriesView.as_view(),
       name='categories'
   ),

   path(
       'projects/<int:pk>/attachments.xml',
       view=DocumentsView.as_view(),
       name='documents'
   ),
]
