from django.conf.urls import patterns, url
from .views import DocumentView, DownloadDocument

urlpatterns = patterns('',
                       url(
                           regex=r'^(?P<pk>\d+)$',
                           view=DocumentView.as_view(),
                           name='document'
                       ),
                       url(
                           regex=r'^(?P<pk>[a-fA-F0-9]{32})/download$',
                           view=DownloadDocument.as_view(),
                           name='download_document'
                       ),
)
