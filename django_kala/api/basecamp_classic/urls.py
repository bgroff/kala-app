from django.urls import path, include

from .companies import urls as company_urls
from .people import urls as people_urls
from .projects import urls as project_urls

app_name='basecamp_classic'

urlpatterns = [
    path(
        '',
        include(company_urls),
    ),
    path(
        '',
        include(people_urls),
    ),
    path(
        '',
        include(project_urls),
    ),
]
