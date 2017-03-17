from django.conf.urls import url
from .views import *

urlpatterns = [
   url(
       regex=r'^companies.xml$',
       view=CompaniesView.as_view(),
       name='companies'
   ),

   url(
       regex=r'^companies/(?P<pk>\d+).xml$',
       view=CompanyView.as_view(),
       name='company'
   ),

   url(
       regex=r'^companies/(?P<pk>\d+)/people.xml$',
       view=PeopleView.as_view(),
       name='people'
   ),
]
