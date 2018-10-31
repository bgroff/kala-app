import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND

from projects.models import Category
from organizations.views.tests import setup, login, user_permissions_test_manage


@pytest.mark.django_db
def test_user_permissions_for_organization_details():
    user, organization, client = setup()
    user_permissions_test_manage(
        view='organizations:details',
        client=client,
        user=user,
        organization=organization,
        args=[organization.pk]
    )


@pytest.mark.django_db
def test_updated_details():
    user, organization, client = setup()
    organization.add_manage(user)
    assert login(client, user)

    # Valid case
    response = client.post(
        path=reverse('organizations:details', args=[organization.pk]),
        data={
            'name': 'Test Organization',
        },
        follow=True
    )
    assert response.redirect_chain[0][0] == reverse('organizations:details', args=[organization.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND

    organization.refresh_from_db()
    assert organization.name == 'Test Organization'

    # Invalid form
    response = client.post(
        path=reverse('organizations:details', args=[organization.pk]),
        data={
            'foo': 'bar',
        }
    )
    assert response.status_code == HTTP_200_OK
