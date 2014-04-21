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
       include('companies.urls'),
   ),

   url(
       r'^documents/',
       include('documents.urls'),
   ),

   url(
       r'^accounts/',
       include('accounts.urls'),
   ),

   url(
       r'^projects/',
       include('projects.urls'),
   ),

   url(
       r'^import/',
       include('bc_import.urls'),
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
