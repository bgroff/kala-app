from django.test import Client
from django.urls import reverse
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_302_FOUND

from auth.tests.factories import UserFactory
from documents.tests.factories import DocumentFactory
from organizations.tests.factories import OrganizationFactory
from projects.tests.factories import ProjectFactory


def setup():
    user = UserFactory.create()
    organization = OrganizationFactory.create()
    project = ProjectFactory.create(organization=organization)
    document = DocumentFactory.create(project=project)

    return user, organization, project, document, Client()


def login(client, user):
    user.set_password('test')
    user.save()
    return client.login(username=user.email, password='test')


def user_permissions_test(view, client, user, organization, project, document, args):
    # Not logged in should redirect to the login page
    response = client.get(reverse(view, args=args), follow=True)
    assert response.redirect_chain[0][0] == '{0}?next={1}'.format(
        reverse('users:login'),
        reverse(view, args=args)
    )
    assert response.redirect_chain[0][1] == HTTP_302_FOUND

    assert login(client, user)

    response = client.get(reverse(view, args=args))
    assert response.status_code == HTTP_403_FORBIDDEN

    # Test correct permissions
    organization.add_manage(user)
    response = client.get(reverse(view, args=args))
    assert response.status_code == HTTP_200_OK
    organization.delete_manage(user)

    project.add_manage(user)
    response = client.get(reverse(view, args=args))
    assert response.status_code == HTTP_200_OK
    project.delete_manage(user)

    document.add_manage(user)
    response = client.get(reverse(view, args=args))
    assert response.status_code == HTTP_200_OK
    document.delete_manage(user)

    # Super user does what they want
    user.is_superuser = True
    user.save()
    response = client.get(reverse(view, args=args))
    assert response.status_code == HTTP_200_OK
    user.is_superuser = False
    user.save()

    # Test that other permissions do not work
    organization.add_create(user)
    organization.add_invite(user)
    response = client.get(reverse(view, args=args))
    assert response.status_code == HTTP_403_FORBIDDEN
    organization.delete_create(user)
    organization.delete_invite(user)

    project.add_create(user)
    project.add_invite(user)
    response = client.get(reverse(view, args=args))
    assert response.status_code == HTTP_403_FORBIDDEN
    project.delete_create(user)
    project.delete_invite(user)

    document.add_create(user)
    document.add_invite(user)
    response = client.get(reverse(view, args=args))
    assert response.status_code == HTTP_403_FORBIDDEN
    document.delete_create(user)
    document.delete_invite(user)

