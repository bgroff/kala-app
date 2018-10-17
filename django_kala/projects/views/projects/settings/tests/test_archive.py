import pytest
from django.urls import reverse
from rest_framework.status import HTTP_302_FOUND

from projects.views.projects.tests import setup, login, user_permissions_test_manage


@pytest.mark.django_db
def test_user_permissions_for_document_archive():
    user, organization, project, client = setup()
    user_permissions_test_manage(
        view='projects:archive',
        client=client,
        user=user,
        organization=organization,
        project=project,
        args=[project.pk]
    )


@pytest.mark.django_db
def test_archive():
    user, organization, project, client = setup()
    project.add_manage(user)
    assert login(client, user)

    # Valid case
    response = client.post(
        path=reverse('projects:archive', args=[project.pk]),
        data={
            'archive': 'Test Project',
        },
        follow=True
    )
    assert response.redirect_chain[0][0] == reverse('projects:projects')
    assert response.redirect_chain[0][1] == HTTP_302_FOUND

    project.refresh_from_db()
    assert project.is_active == False
