import pytest
from django.urls import reverse
from rest_framework.status import HTTP_302_FOUND, HTTP_403_FORBIDDEN, HTTP_200_OK

from documents.tests.factories import DocumentVersionFactory
from projects.views.documents.tests import setup, login


@pytest.mark.django_db
def test_document_download():
    user, organization, project, document, client = setup()

    version = DocumentVersionFactory(document=document)
    view = 'projects:download'
    args = [project.pk, document.pk, document.documentversion_set.first().uuid]

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
    response = client.get(reverse(view, args=args), follow=True)
    assert response.redirect_chain[0][0] == 'http://localhost/test_download'
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    organization.delete_manage(user)

    project.add_manage(user)
    response = client.get(reverse(view, args=args), follow=True)
    assert response.redirect_chain[0][0] == 'http://localhost/test_download'
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    project.delete_manage(user)

    document.add_manage(user)
    response = client.get(reverse(view, args=args), follow=True)
    assert response.redirect_chain[0][0] == 'http://localhost/test_download'
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    document.delete_manage(user)

    # Super user does what they want
    user.is_superuser = True
    user.save()
    response = client.get(reverse(view, args=args), follow=True)
    assert response.redirect_chain[0][0] == 'http://localhost/test_download'
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    user.is_superuser = False
    user.save()

    organization.add_create(user)
    response = client.get(reverse(view, args=args), follow=True)
    assert response.redirect_chain[0][0] == 'http://localhost/test_download'
    assert response.redirect_chain[0][1] == HTTP_302_FOUND

    organization.delete_create(user)

    organization.add_invite(user)
    response = client.get(reverse(view, args=args), follow=True)
    assert response.redirect_chain[0][0] == 'http://localhost/test_download'
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    organization.delete_invite(user)

    project.add_create(user)
    response = client.get(reverse(view, args=args), follow=True)
    assert response.redirect_chain[0][0] == 'http://localhost/test_download'
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    project.delete_create(user)

    project.add_invite(user)
    response = client.get(reverse(view, args=args), follow=True)
    assert response.redirect_chain[0][0] == 'http://localhost/test_download'
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    project.delete_invite(user)

    document.add_create(user)
    response = client.get(reverse(view, args=args), follow=True)
    assert response.redirect_chain[0][0] == 'http://localhost/test_download'
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    document.delete_create(user)

    document.add_invite(user)
    response = client.get(reverse(view, args=args), follow=True)
    assert response.redirect_chain[0][0] == 'http://localhost/test_download'
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    document.delete_invite(user)
