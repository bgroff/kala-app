from django.conf.urls import url, include

urlpatterns = [
    url(
        r'^',
        include('basecamp_classic.companies.urls'),
    ),
    url(
        r'^',
        include('basecamp_classic.people.urls'),
    ),
    url(
        r'^',
        include('basecamp_classic.projects.urls'),
    ),
]
