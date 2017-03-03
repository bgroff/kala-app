from django.conf.urls import url, include

urlpatterns = [
    url(
        r'^',
        include('basecamp_classic.people.urls', namespace='basecamp_classic_people')
    ),
]
