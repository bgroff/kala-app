from django.urls import path
from .views import *

urlpatterns = [
   path(
       'me.xml',
       view=MeView.as_view(),
       name='me'
   ),

   path(
       'people.xml',
       view=PeopleView.as_view(),
       name='people'
   ),

   path(
       'people/<int:pk>.xml',
       view=PersonView.as_view(),
       name='people'
   ),
]
