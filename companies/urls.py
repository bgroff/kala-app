from django.conf.urls import patterns, url
from .views import CompanyView

urlpatterns = patterns('',
                       url(
                           regex=r'^(?P<pk>\d+)$',
                           view=CompanyView.as_view(),
                           name='company',
                       ),
)
