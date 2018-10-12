import pytest
from django.urls import reverse
from rest_framework.status import HTTP_302_FOUND, HTTP_403_FORBIDDEN

from projects.views.documents.tests import setup, user_permissions_test_create, login


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'memory://',
    }


@pytest.mark.django_db
def test_user_permissions_for_document():
    user, organization, project, document, client = setup()
    user_permissions_test_create(
        view='projects:document',
        client=client,
        user=user,
        organization=organization,
        project=project,
        document=document,
        args=[project.pk, document.pk]
    )


@pytest.mark.django_db
def test_user_permissions_for_document_export():
    user, organization, project, document, client = setup()
    # Not logged in should redirect to the login page
    response = client.get(reverse('projects:export_document', args=[project.pk, document.pk]), follow=True)
    assert response.redirect_chain[0][0] == '{0}?next={1}'.format(
        reverse('users:login'),
        reverse('projects:export_document', args=[project.pk, document.pk])
    )
    assert response.redirect_chain[0][1] == HTTP_302_FOUND

    assert login(client, user)

    response = client.get(reverse('projects:export_document', args=[project.pk, document.pk]))
    assert response.status_code == HTTP_403_FORBIDDEN

    # Test correct permissions
    organization.add_manage(user)
    response = client.get(reverse('projects:export_document', args=[project.pk, document.pk]), follow=True)
    assert response.redirect_chain[0][0] == reverse('projects:document', args=[project.pk, document.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    organization.delete_manage(user)

    project.add_manage(user)
    response = client.get(reverse('projects:export_document', args=[project.pk, document.pk]), follow=True)
    assert response.redirect_chain[0][0] == reverse('projects:document', args=[project.pk, document.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    project.delete_manage(user)

    document.add_manage(user)
    response = client.get(reverse('projects:export_document', args=[project.pk, document.pk]), follow=True)
    assert response.redirect_chain[0][0] == reverse('projects:document', args=[project.pk, document.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    document.delete_manage(user)

    # Super user does what they want
    user.is_superuser = True
    user.save()
    response = client.get(reverse('projects:export_document', args=[project.pk, document.pk]), follow=True)
    assert response.redirect_chain[0][0] == reverse('projects:document', args=[project.pk, document.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    user.is_superuser = False
    user.save()

    organization.add_create(user)
    response = client.get(reverse('projects:export_document', args=[project.pk, document.pk]), follow=True)
    assert response.redirect_chain[0][0] == reverse('projects:document', args=[project.pk, document.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    organization.delete_create(user)

    organization.add_invite(user)
    response = client.get(reverse('projects:export_document', args=[project.pk, document.pk]), follow=True)
    assert response.redirect_chain[0][0] == reverse('projects:document', args=[project.pk, document.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    organization.delete_invite(user)

    project.add_create(user)
    response = client.get(reverse('projects:export_document', args=[project.pk, document.pk]), follow=True)
    assert response.redirect_chain[0][0] == reverse('projects:document', args=[project.pk, document.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    project.delete_create(user)

    project.add_invite(user)
    response = client.get(reverse('projects:export_document', args=[project.pk, document.pk]), follow=True)
    assert response.redirect_chain[0][0] == reverse('projects:document', args=[project.pk, document.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    project.delete_invite(user)

    document.add_create(user)
    response = client.get(reverse('projects:export_document', args=[project.pk, document.pk]), follow=True)
    assert response.redirect_chain[0][0] == reverse('projects:document', args=[project.pk, document.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    document.delete_create(user)

    document.add_invite(user)
    response = client.get(reverse('projects:export_document', args=[project.pk, document.pk]), follow=True)
    assert response.redirect_chain[0][0] == reverse('projects:document', args=[project.pk, document.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    document.delete_invite(user)
