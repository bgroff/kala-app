import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND

from projects.models import Category
from projects.views.projects.tests import setup, login, user_permissions_test_manage


@pytest.mark.django_db
def test_user_permissions_for_document_details():
    user, organization, project, client = setup()
    user_permissions_test_manage(
        view='projects:details',
        client=client,
        user=user,
        organization=organization,
        project=project,
        args=[project.pk]
    )


@pytest.mark.django_db
def test_updated_details():
    user, organization, project, client = setup()
    project.add_manage(user)
    assert login(client, user)

    # Valid case
    category = Category.objects.create(name='Test Category', project=project)
    response = client.post(
        path=reverse('projects:details', args=[project.pk]),
        data={
            'name': 'Test Project',
            'description': 'Test Description',
            'tags': ['test, tags']
        },
        follow=True
    )
    assert response.redirect_chain[0][0] == reverse('projects:details', args=[project.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND

    project.refresh_from_db()
    assert project.name == 'Test Project'
    assert project.description == 'Test Description'
    assert len(project.tags.all()) == 2

    # Invalid form
    response = client.post(
        path=reverse('projects:details', args=[project.pk]),
        data={
            'foo': 'bar',
        }
    )
    assert response.status_code == HTTP_200_OK
