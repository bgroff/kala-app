from django.urls import path, include

from .projects import urls as project_urls
from .organizations import urls as organization_urls

app_name='v1'

urlpatterns = [
    # url(
    #     r'^',
    #     include(auth_urls),
    # ),

    path(
        '',
        include(project_urls),
    ),

    path(
        '',
        include(organization_urls),
    ),
]


