from django.conf.urls import url, include

from .companies import urls as company_urls
from .people import urls as people_urls
from .projects import urls as project_urls

urlpatterns = [
    url(
        r'^',
        include(company_urls),
    ),
    url(
        r'^',
        include(people_urls),
    ),
    url(
        r'^',
        include(project_urls),
    ),
]
