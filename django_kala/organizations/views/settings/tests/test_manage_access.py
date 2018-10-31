import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND

from auth.tests.factories import UserFactory
from projects.models import ProjectPermission
from organizations.views.tests import setup, login, user_permissions_test_manage


@pytest.mark.django_db
def test_user_permissions_for_project_manage_access():
    user, organization, client = setup()
    user_permissions_test_manage(
        view='organizations:manage_access',
        client=client,
        user=user,
        organization=organization,
        args=[organization.pk]
    )


@pytest.mark.django_db
def test_project_manage_access():
    user, organization, client = setup()
    # Add superuser so the other user can be seen.
    user.is_superuser = True
    user.save()
    organization.add_manage(user)
    assert login(client, user)

    other_user = UserFactory()

    # Valid create case
    assert organization.can_create(other_user) == False
    response = client.post(
        path=reverse('organizations:manage_access', args=[organization.pk]),
        data={
            'can_create_{0}'.format(other_user.pk): True,
        },
        follow=True
    )
    assert response.redirect_chain[0][0] == reverse('organizations:manage_access', args=[organization.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    assert organization.can_create(other_user) == True

    # Remove Create
    response = client.post(
        path=reverse('organizations:manage_access', args=[organization.pk]),
        data={
            'none_{0}'.format(other_user.pk): True,
        },
        follow=True
    )
    assert response.redirect_chain[0][0] == reverse('organizations:manage_access', args=[organization.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    assert organization.can_create(other_user) == False

    # Valid invite case
    assert organization.can_invite(other_user) == False
    response = client.post(
        path=reverse('organizations:manage_access', args=[organization.pk]),
        data={
            'can_invite_{0}'.format(other_user.pk): True,
        },
        follow=True
    )
    assert response.redirect_chain[0][0] == reverse('organizations:manage_access', args=[organization.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    assert organization.can_invite(other_user) == True

    # Remove invite
    response = client.post(
        path=reverse('organizations:manage_access', args=[organization.pk]),
        data={
            'none_{0}'.format(other_user.pk): True,
        },
        follow=True
    )
    assert response.redirect_chain[0][0] == reverse('organizations:manage_access', args=[organization.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    assert organization.can_invite(other_user) == False

    # Valid manage case
    assert organization.can_manage(other_user) == False
    response = client.post(
        path=reverse('organizations:manage_access', args=[organization.pk]),
        data={
            'can_manage_{0}'.format(other_user.pk): True,
        },
        follow=True
    )
    assert response.redirect_chain[0][0] == reverse('organizations:manage_access', args=[organization.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    assert organization.can_manage(other_user) == True

    # Remove manage
    response = client.post(
        path=reverse('organizations:manage_access', args=[organization.pk]),
        data={
            'none_{0}'.format(other_user.pk): True,
        },
        follow=True
    )
    assert response.redirect_chain[0][0] == reverse('organizations:manage_access', args=[organization.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    assert organization.can_manage(other_user) == False


@pytest.mark.django_db
def test_project_manage_access_no_data():
    user, organization, client = setup()
    organization.add_manage(user)
    assert login(client, user)

    # Send an invalid payload
    response = client.post(
        path=reverse('organizations:manage_access', args=[organization.pk]),
        data={
        },
        follow=True
    )
    assert response.status_code == HTTP_200_OK
