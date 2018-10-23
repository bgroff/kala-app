import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND

from projects.views.projects.tests import setup, user_permissions_test_create, login

User = get_user_model()


@pytest.mark.django_db
def test_user_permissions_for_new_document():
    user, organization, project, client = setup()
    user_permissions_test_create(
        view='projects:new_document',
        client=client,
        user=user,
        organization=organization,
        project=project,
        args=[project.pk]
    )


@pytest.mark.django_db
def test_new_document():
    user, organization, project, client = setup()
    project.add_create(user)
    assert login(client, user)

    with open('projects/views/documents/tests/test_file.txt') as test_file:
        assert len(user.get_documents()) == 0
        response = client.post(
            path=reverse('projects:new_document', args=[project.pk]),
            data={
                'description': 'Test Description',
                'file': test_file,
            },
            follow=True
        )
        documents = user.get_documents()
        assert response.redirect_chain[0][0] == reverse('projects:document', args=[project.pk, documents[0].pk])
        assert response.redirect_chain[0][1] == HTTP_302_FOUND
        assert len(documents) == 1
        assert documents[0].project.pk == project.pk


@pytest.mark.django_db
def test_new_document_fail_validation():
    user, organization, project, client = setup()
    project.add_create(user)
    assert login(client, user)

    with open('projects/views/documents/tests/test_file.txt') as test_file:
        assert len(user.get_documents()) == 0
        response = client.post(
            path=reverse('projects:new_document', args=[project.pk]),
            data={
            },
        )
        assert len(user.get_documents()) == 0
        assert response.status_code == HTTP_200_OK
