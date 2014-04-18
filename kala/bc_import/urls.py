from django.conf.urls import patterns, url
from .views import BasecampAuthorize, BasecampImport, BasecampUnauthorize, BasecampDownloadDocument

urlpatterns = patterns('',
   url(
       regex=r'^authorize$',
       view=BasecampAuthorize.as_view(),
       name='basecamp_authorize'
   ),
   url(
       regex=r'^unauthorize$',
       view=BasecampUnauthorize.as_view(),
       name='basecamp_unauthorize'
   ),
   url(
       regex=r'^$',
       view=BasecampImport.as_view(),
       name='basecamp_import'
   ),
   url(
       regex=r'^(?P<pk>[a-fA-F0-9]{32})/download$',
       view=BasecampDownloadDocument.as_view(),
       name='basecamp_download_document'
   ),
)
