import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework.status import HTTP_200_OK

from projects.views.projects.tests import setup, user_permissions_test_invite, login


User = get_user_model()

@pytest.mark.django_db
def test_user_permissions_for_project():
    user, organization, project, client = setup()
    user_permissions_test_invite(
        view='projects:project_invite_user',
        client=client,
        user=user,
        organization=organization,
        project=project,
        args=[project.pk]
    )


@pytest.mark.django_db
def test_project_invite_user_no_data():
    user, organization, project, client = setup()
    project.add_invite(user)
    assert login(client, user)

    response = client.post(
        path=reverse('projects:project_invite_user', args=[project.pk]),
        data={
        },
        follow=True
    )
    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_project_invite_user():
    user, organization, project, client = setup()
    project.add_invite(user)
    assert login(client, user)

    response = client.post(
        path=reverse('projects:project_invite_user', args=[project.pk]),
        data={
            'email': 'test.user@test.com',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'creator'
        },
        follow=True
    )
    assert response.status_code == HTTP_200_OK

    new_user = User.objects.get(email='test.user@test.com')
    assert project.can_create(new_user)
    assert not project.can_invite(new_user)
    assert not project.can_manage(new_user)


@pytest.mark.django_db
def test_project_invite_user_as_collaborator():
    user, organization, project, client = setup()
    project.add_invite(user)
    assert login(client, user)

    response = client.post(
        path=reverse('projects:project_invite_user', args=[project.pk]),
        data={
            'email': 'test.user@test.com',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'collaborator'
        },
        follow=True
    )
    assert response.status_code == HTTP_200_OK

    new_user = User.objects.get(email='test.user@test.com')
    assert project.can_create(new_user)
    assert project.can_invite(new_user)
    assert not project.can_manage(new_user)


@pytest.mark.django_db
def test_project_invite_user_as_manager():
    user, organization, project, client = setup()
    project.add_invite(user)
    assert login(client, user)

    # Not a manager so this should fail
    response = client.post(
        path=reverse('projects:project_invite_user', args=[project.pk]),
        data={
            'email': 'test.user@test.com',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'manager'
        },
        follow=True
    )
    assert response.status_code == HTTP_200_OK
    with pytest.raises(User.DoesNotExist):
        User.objects.get(email='test.user@test.com')

    project.add_invite(user)

    # Now we can do this
    project.add_manage(user)
    response = client.post(
        path=reverse('projects:project_invite_user', args=[project.pk]),
        data={
            'email': 'test.user@test.com',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'manager'
        },
        follow=True
    )
    assert response.status_code == HTTP_200_OK

    new_user = User.objects.get(email='test.user@test.com')
    assert project.can_create(new_user)
    assert project.can_invite(new_user)
    assert project.can_manage(new_user)


@pytest.mark.django_db
def test_project_invite_user_sends_email():
    user, organization, project, client = setup()
    project.add_manage(user)
    assert login(client, user)

    # Send an invalid payload
    response = client.post(
        path=reverse('projects:project_invite_user', args=[project.pk]),
        data={
            'email': 'test.user@test.com',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'manager'
        },
        follow=True
    )
    assert response.status_code == HTTP_200_OK

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == 'Invitation to collaborate'
