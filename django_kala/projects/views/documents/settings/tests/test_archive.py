import pytest
from django.urls import reverse
from rest_framework.status import HTTP_302_FOUND

from projects.views.documents.tests import setup, login, user_permissions_test_manage


@pytest.mark.django_db
def test_user_permissions_for_document_archive():
    user, organization, project, document, client = setup()
    user_permissions_test_manage(
        view='projects:document_archive',
        client=client,
        user=user,
        organization=organization,
        project=project,
        document=document,
        args=[project.pk, document.pk]
    )


@pytest.mark.django_db
def test_archive():
    user, organization, project, document, client = setup()
    document.add_manage(user)
    assert login(client, user)

    # Valid case
    response = client.post(
        path=reverse('projects:document_archive', args=[project.pk, document.pk]),
        data={
            'archive': 'Test Project',
        },
        follow=True
    )
    assert response.redirect_chain[0][0] == reverse('projects:document_archive', args=[project.pk, document.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND

    document.refresh_from_db()
    assert document.is_active == False
