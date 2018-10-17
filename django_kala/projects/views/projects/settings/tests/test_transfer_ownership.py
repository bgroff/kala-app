import pytest
from django.urls import reverse
from rest_framework.status import HTTP_302_FOUND, HTTP_200_OK

from organizations.tests.factories import OrganizationFactory
from projects.views.projects.tests import setup, login, user_permissions_test_manage


@pytest.mark.django_db
def test_user_permissions_for_document_archive():
    user, organization, project, client = setup()
    user_permissions_test_manage(
        view='projects:transfer_ownership',
        client=client,
        user=user,
        organization=organization,
        project=project,
        args=[project.pk]
    )


@pytest.mark.django_db
def test_transfer_ownership():
    user, organization, project, client = setup()
    project.add_manage(user)
    assert login(client, user)

    # Test that the user does not have permissions yet.
    new_organization = OrganizationFactory()

    # Valid case
    assert project.organization.pk == organization.pk
    response = client.post(
        path=reverse('projects:transfer_ownership', args=[project.pk]),
        data={
            'organization': new_organization.pk,
        },
        follow=True
    )
    assert response.status_code == HTTP_200_OK
    project.refresh_from_db()
    assert project.organization.pk != new_organization.pk


    # Test that if the user does not have enough permissions, that things do not work.
    new_organization.add_create(user)
    # Valid case
    assert project.organization.pk == organization.pk
    response = client.post(
        path=reverse('projects:transfer_ownership', args=[project.pk]),
        data={
            'organization': new_organization.pk,
        },
        follow=True
    )
    assert response.status_code == HTTP_200_OK

    project.refresh_from_db()
    assert project.organization.pk == organization.pk
    new_organization.delete_create(user)

    # Test that if the user does not have enough permissions, that things do not work.
    new_organization.add_invite(user)
    # Valid case
    assert project.organization.pk == organization.pk
    response = client.post(
        path=reverse('projects:transfer_ownership', args=[project.pk]),
        data={
            'organization': new_organization.pk,
        },
        follow=True
    )
    assert response.status_code == HTTP_200_OK

    project.refresh_from_db()
    assert project.organization.pk == organization.pk
    new_organization.delete_invite(user)

    # Now test that they do.
    new_organization.add_manage(user)

    # Valid case
    assert project.organization.pk == organization.pk
    response = client.post(
        path=reverse('projects:transfer_ownership', args=[project.pk]),
        data={
            'organization': new_organization.pk,
        },
        follow=True
    )
    assert response.redirect_chain[0][0] == reverse('projects:transfer_ownership', args=[project.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND

    project.refresh_from_db()
    assert project.organization.pk == new_organization.pk
