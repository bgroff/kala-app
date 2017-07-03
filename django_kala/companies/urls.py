from django.conf.urls import url
from .views import CompaniesView, NewCompanyView, DetailsView

urlpatterns = [
    url(
        regex=r'^$',
        view=CompaniesView.as_view(),
        name='organizations',
    ),

    url(
        regex=r'^(?P<pk>\d+)/$',
        view=CompaniesView.as_view(),
        name='organization',
    ),

    url(
        regex=r'^new$',
        view=NewCompanyView.as_view(),
        name='new_organization',
    ),

    url(
        regex=r'^(?P<pk>\d+)/settings/details$',
        view=DetailsView.as_view(),
        name='details'
    ),

]
