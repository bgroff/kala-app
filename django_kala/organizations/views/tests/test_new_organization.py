import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND, HTTP_403_FORBIDDEN

from organizations.views.tests import setup, user_permissions_test_create, login
from organizations.tests.factories import OrganizationFactory

User = get_user_model()


@pytest.mark.django_db
def test_user_permissions_for_new_organization():
    user, organization, client = setup()
    # Not logged in should redirect to the login page
    response = client.get(reverse('organizations:new_organization'), follow=True)
    assert response.redirect_chain[0][0] == '{0}?next={1}'.format(
        reverse('users:login'),
        reverse('organizations:new_organization')
    )
    assert response.redirect_chain[0][1] == HTTP_302_FOUND

    assert login(client, user)

    response = client.get(reverse('organizations:new_organization'))
    assert response.status_code == HTTP_403_FORBIDDEN

    # Super user does what they want
    user.is_superuser = True
    user.save()
    response = client.get(reverse('organizations:new_organization'))
    assert response.status_code == HTTP_200_OK
    user.is_superuser = False
    user.save()


@pytest.mark.django_db
def test_new_organization():
    user, organization, client = setup()
    user.is_superuser = True
    user.save()
    assert login(client, user)

    assert len(user.get_organizations()) == 2
    response = client.post(
        path=reverse('organizations:new_organization'),
        data={
            'name': 'Test Organization',
            'website': 'http://example.com',
        },
        follow=True
    )
    organizations = user.get_organizations()
    assert response.redirect_chain[0][0] == reverse('organizations:organization', args=[organizations.get(name='Test Organization').pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    assert len(organizations) == 3


@pytest.mark.django_db
def test_new_organization_fail_validation():
    user, organization, client = setup()
    user.is_superuser = True
    user.save()
    assert login(client, user)

    assert user.get_organizations().count() == 2
    response = client.post(
        path=reverse('organizations:new_organization'),
        data={
        },
    )
    assert user.get_organizations().count() == 2
    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_new_organization_no_permissions():
    user, organization, client = setup()
    assert login(client, user)

    assert len(user.get_organizations()) == 0
    response = client.post(
        path=reverse('organizations:new_organization'),
        data={
        },
    )
    assert response.status_code == HTTP_403_FORBIDDEN

    organization = OrganizationFactory()
    organization.add_manage(user)
    assert len(user.get_organizations()) == 1
    response = client.post(
        path=reverse('organizations:new_organization'),
        data={
            'name': 'Test organization',
        },
    )
    assert response.status_code == HTTP_403_FORBIDDEN
    assert len(user.get_organizations()) == 1
