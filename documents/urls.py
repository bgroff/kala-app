from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from documents.views import Projects, ProjectView

urlpatterns = patterns('',
    url(r'^projects$', login_required(Projects.as_view()), name='projects'),
    url(r'^projects/(?P<pk>\d+)', ProjectView.as_view(), name='project')
)
