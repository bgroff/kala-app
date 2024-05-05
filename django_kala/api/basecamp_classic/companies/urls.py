from django.urls import path
from .views import *

urlpatterns = [
   path(
       'companies.xml',
       view=CompaniesView.as_view(),
       name='companies'
   ),

   path(
       'companies/<int:pk>.xml',
       view=CompanyView.as_view(),
       name='company'
   ),

   path(
       'companies/<int:pk>/people.xml',
       view=PeopleView.as_view(),
       name='people'
   ),
]
