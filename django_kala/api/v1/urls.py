from django.conf.urls import url, include

from .auth import urls as auth_urls
from .projects import urls as project_urls
from .organizations import urls as organization_urls

app_name='v1'

urlpatterns = [
    # url(
    #     r'^',
    #     include(auth_urls),
    # ),

    url(
        r'^',
        include(project_urls),
    ),

    # url(
    #     r'^',
    #     include(organization_urls),
    # ),
]


