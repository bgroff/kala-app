from django.conf.urls import patterns, include, url
from .views import Home, LicenseView, UserDocumentationView

urlpatterns = patterns('',
   url(
       regex=r'^$',
       view=Home.as_view(),
       name='home'
   ),

   url(
       r'^companies/',
       include('kala.companies.urls'),
   ),

   url(
       r'^documents/',
       include('kala.documents.urls'),
   ),

   url(
       r'^accounts/',
       include('kala.accounts.urls'),
   ),

   url(
       r'^projects/',
       include('kala.projects.urls'),
   ),

   url(
       r'^import/',
       include('kala.bc_import.urls'),
   ),

    url(
        regex=r'^license$',
        view=LicenseView.as_view(),
        name='license',
    ),
    url(
        regex=r'^user_documentation$',
        view=UserDocumentationView.as_view(),
        name='user_documentation',
    ),
)
