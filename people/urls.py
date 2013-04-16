from django.conf.urls import patterns, url
from .views import PeopleView

urlpatterns = patterns('',
                       url(regex=r'^$',
                           view=PeopleView.as_view(),
                           name='people',
                       ),
)
