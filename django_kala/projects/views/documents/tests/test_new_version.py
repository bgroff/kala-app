import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND

from projects.views.documents.tests import setup, user_permissions_test_create, login


User = get_user_model()

@pytest.mark.django_db
def test_user_permissions_for_new_version():
    user, organization, project, document, client = setup()
    user_permissions_test_create(
        view='projects:new_version',
        client=client,
        user=user,
        organization=organization,
        project=project,
        document=document,
        args=[project.pk, document.pk]
    )


@pytest.mark.django_db
def test_document_new_version():
    user, organization, project, document, client = setup()
    document.add_manage(user)
    assert login(client, user)

    with open('projects/views/documents/tests/test_file.txt') as test_file:
        assert document.documentversion_set.first() is None
        response = client.post(
            path=reverse('projects:new_version', args=[project.pk, document.pk]),
            data={
                'description': 'Test Description',
                'file': test_file,
            },
            follow=True
        )
        assert response.redirect_chain[0][0] == reverse('projects:document', args=[project.pk, document.pk])
        assert response.redirect_chain[0][1] == HTTP_302_FOUND
        version = document.documentversion_set.first()
        assert version is not None
        assert version.name == 'test_file.txt'


@pytest.mark.django_db
def test_document_new_version_fail_validation():
    user, organization, project, document, client = setup()
    document.add_manage(user)
    assert login(client, user)

    with open('projects/views/documents/tests/test_file.txt') as test_file:
        assert document.documentversion_set.first() is None
        response = client.post(
            path=reverse('projects:new_version', args=[project.pk, document.pk]),
            data={
            },
        )
        assert document.documentversion_set.first() is None
        assert response.status_code == HTTP_200_OK
