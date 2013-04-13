from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from documents.views import Projects, ProjectView, Documents, DocumentView, DownloadDocument, People, CompanyView, ProjectPermissions

urlpatterns = patterns('',
    url(r'^projects$', login_required(Projects.as_view()), name='projects'),
    url(r'^projects/(?P<pk>\d+)$', login_required(ProjectView.as_view()), name='project'),
    url(r'^projects/(?P<pk>\d+)/permissions$', login_required(ProjectPermissions.as_view()), name='permissions'),

    url(r'^documents$', login_required(Documents.as_view()), name='documents'),
    url(r'^documents/(?P<pk>\d+)$', DocumentView.as_view(), name='document'),
    url(r'^documents/(?P<pk>[a-fA-F0-9]{32})/download$', DownloadDocument.as_view(), name='download_document'),

    url(r'^people$', login_required(People.as_view()), name='people'),
    url(r'^companies/(?P<pk>\d+)$', login_required(CompanyView.as_view()), name='company'),
)
