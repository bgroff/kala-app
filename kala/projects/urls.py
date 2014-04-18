from django.conf.urls import patterns, url
from .views import ProjectsView, ProjectView, ProjectPermissions

urlpatterns = patterns('',
                       url(
                           regex=r'^$',
                           view=ProjectsView.as_view(),
                           name='projects'
                       ),
                       url(
                           regex=r'^(?P<pk>\d+)$',
                           view=ProjectView.as_view(),
                           name='project'
                       ),
                       url(
                           regex=r'^(?P<pk>\d+)/permissions$',
                           view=ProjectPermissions.as_view(),
                           name='permissions'),
)
