import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND

from projects.models import Category
from . import setup, login, user_permissions_test


@pytest.mark.django_db
def test_user_permissions_for_document_details():
    user, organization, project, document, client = setup()
    user_permissions_test(
        view='projects:document_details',
        client=client,
        user=user,
        organization=organization,
        project=project,
        document=document,
        args=[project.pk, document.pk]
    )


@pytest.mark.django_db
def test_updated_details():
    user, organization, project, document, client = setup()
    document.add_manage(user)
    assert login(client, user)

    # Valid case
    category = Category.objects.create(name='Test Category', project=project, type='test')
    response = client.post(
        path=reverse('projects:document_details', args=[project.pk, document.pk]),
        data={
            'name': 'Test Project',
            'category': category.pk,
            'tags': ['test, tags']
        },
        follow=True
    )
    assert response.redirect_chain[0][0] == reverse('projects:document_details', args=[project.pk, document.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND

    document.refresh_from_db()
    assert document.name == 'Test Project'
    assert document.category.name == category.name
    assert len(document.tags.all()) == 2

    # Invalid form
    response = client.post(
        path=reverse('projects:document_details', args=[project.pk, document.pk]),
        data={
            'foo': 'bar',
        }
    )
    assert response.status_code == HTTP_200_OK
