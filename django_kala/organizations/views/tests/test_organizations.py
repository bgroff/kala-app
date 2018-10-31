import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND

from organizations.views.tests import setup, login

User = get_user_model()


@pytest.mark.django_db
def test_organizations():
    user, organization, client = setup()

    response = client.get(
        path=reverse('organizations:organizations')
    )
    assert response.status_code == HTTP_302_FOUND

    assert login(client, user)

    response = client.get(
        path=reverse('organizations:organizations')
    )
    assert response.status_code == HTTP_200_OK
