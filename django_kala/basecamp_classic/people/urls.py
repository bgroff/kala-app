from django.conf.urls import url
from .views import *

urlpatterns = [
   url(
       regex=r'^me.xml$',
       view=MeView.as_view(),
       name='me'
   ),

   url(
       regex=r'^people.xml$',
       view=PeopleView.as_view(),
       name='people'
   ),

   url(
       regex=r'^people/(?P<pk>\d+).xml$',
       view=PersonView.as_view(),
       name='people'
   ),
]
