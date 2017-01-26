from django.conf.urls import url
from .views import CompanyView

urlpatterns = [
   url(
       regex=r'^(?P<pk>\d+)/$',
       view=CompanyView.as_view(),
       name='company',
   ),
]
