import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND, HTTP_403_FORBIDDEN

from organizations.views.tests import setup, user_permissions_test_create, login
from projects.tests.factories import ProjectFactory

User = get_user_model()


@pytest.mark.django_db
def test_user_permissions_for_new_project():
    user, organization, client = setup()
    user_permissions_test_create(
        view='projects:new_project',
        client=client,
        user=user,
        organization=organization,
        args=[]
    )


@pytest.mark.django_db
def test_new_project():
    user, organization, client = setup()
    organization.add_create(user)
    assert login(client, user)

    assert len(user.get_projects()) == 0
    response = client.post(
        path=reverse('projects:new_project'),
        data={
            'name': 'Test Project',
            'description': 'Test Description',
            'organization': organization.pk
        },
        follow=True
    )
    projects = user.get_projects()
    assert response.redirect_chain[0][0] == reverse('projects:project', args=[projects[0].pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    assert len(projects) == 1
    assert projects[0].organization.pk == organization.pk


@pytest.mark.django_db
def test_new_project_fail_validation():
    user, organization, client = setup()
    organization.add_create(user)
    assert login(client, user)

    assert len(user.get_projects()) == 0
    response = client.post(
        path=reverse('projects:new_project'),
        data={
        },
    )
    assert len(user.get_projects()) == 0
    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_new_project_no_permissions():
    user, organization, client = setup()
    assert login(client, user)

    assert len(user.get_projects()) == 0
    response = client.post(
        path=reverse('projects:new_project'),
        data={
        },
    )
    assert response.status_code == HTTP_403_FORBIDDEN

    project = ProjectFactory(organization=organization)
    project.add_manage(user)
    assert len(user.get_projects()) == 1
    response = client.post(
        path=reverse('projects:new_project'),
        data={
            'name': 'Test Project',
            'description': 'Test Description',
            'organization': organization.pk
        },
    )
    assert response.status_code == HTTP_403_FORBIDDEN
    assert len(user.get_projects()) == 1
