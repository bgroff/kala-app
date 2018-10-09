import pytest

from documents.tests.factories import DocumentFactory
from projects.tests.factories import ProjectFactory
from organizations.tests.factories import OrganizationFactory

from .factories import UserFactory


@pytest.mark.django_db
def test_user_has_no_permissions():
    user = UserFactory.create()

    # Create some objects that the user should not be able to see
    organization = OrganizationFactory.create()
    project = ProjectFactory.create(organization=organization)
    DocumentFactory.create(project=project)
    UserFactory.create()

    assert len(user.get_organizations()) == 0
    assert len(user.get_projects()) == 0
    assert len(user.get_documents()) == 0
    assert len(user.get_users()) == 0


@pytest.mark.django_db
def test_user_has_superuser():
    user = UserFactory.create(is_superuser=True)

    organization = OrganizationFactory.create()
    project = ProjectFactory.create(organization=organization)
    DocumentFactory.create(project=project)
    UserFactory.create()

    assert len(user.get_organizations()) == 1
    assert len(user.get_projects()) == 1
    assert len(user.get_documents()) == 1
    assert len(user.get_users()) == 2


@pytest.mark.django_db
def test_user_has_organization_permissions():
    user = UserFactory.create()

    organization = OrganizationFactory.create()
    organization.add_create(user)
    project = ProjectFactory.create(organization=organization)
    document = DocumentFactory.create(project=project)

    assert len(user.get_organizations()) == 1
    assert len(user.get_projects()) == 1
    assert len(user.get_documents()) == 1

    assert organization.can_create(user) == True
    assert organization.can_invite(user) == False
    assert organization.can_manage(user) == False

    assert project.can_create(user) == True
    assert project.can_invite(user) == False
    assert project.can_manage(user) == False

    assert document.can_create(user) == True
    assert document.can_invite(user) == False
    assert document.can_manage(user) == False

    organization.delete_create(user)
    organization.add_invite(user)

    assert organization.can_create(user) == True
    assert organization.can_invite(user) == True
    assert organization.can_manage(user) == False

    assert project.can_create(user) == True
    assert project.can_invite(user) == True
    assert project.can_manage(user) == False

    assert document.can_create(user) == True
    assert document.can_invite(user) == True
    assert document.can_manage(user) == False

    organization.delete_invite(user)
    organization.add_manage(user)

    assert organization.can_create(user) == True
    assert organization.can_invite(user) == True
    assert organization.can_manage(user) == True

    assert project.can_invite(user) == True
    assert project.can_create(user) == True
    assert project.can_manage(user) == True

    assert document.can_invite(user) == True
    assert document.can_create(user) == True
    assert document.can_manage(user) == True


@pytest.mark.django_db
def test_user_has_project_permissions():
    user = UserFactory.create()

    organization = OrganizationFactory.create()
    project = ProjectFactory.create(organization=organization)
    project.add_create(user)
    document = DocumentFactory.create(project=project)

    assert len(user.get_organizations()) == 1
    assert len(user.get_projects()) == 1
    assert len(user.get_documents()) == 1

    assert organization.can_manage(user) == False
    assert organization.can_invite(user) == False
    assert organization.can_create(user) == False

    assert project.can_create(user) == True
    assert project.can_invite(user) == False
    assert project.can_manage(user) == False

    assert document.can_create(user) == True
    assert document.can_invite(user) == False
    assert document.can_manage(user) == False

    project.delete_create(user)
    project.add_invite(user)
    assert project.can_create(user) == True
    assert project.can_invite(user) == True
    assert project.can_manage(user) == False

    assert document.can_create(user) == True
    assert document.can_invite(user) == True
    assert document.can_manage(user) == False

    project.delete_create(user)
    project.add_manage(user)
    assert project.can_create(user) == True
    assert project.can_invite(user) == True
    assert project.can_manage(user) == True

    assert document.can_invite(user) == True
    assert document.can_create(user) == True
    assert document.can_manage(user) == True


@pytest.mark.django_db
def test_user_has_document_permissions():
    user = UserFactory.create()

    organization = OrganizationFactory.create()
    project = ProjectFactory.create(organization=organization)
    document = DocumentFactory.create(project=project)
    document.add_create(user)

    assert len(user.get_organizations()) == 1
    assert len(user.get_projects()) == 1
    assert len(user.get_documents()) == 1

    assert organization.can_manage(user) == False
    assert organization.can_invite(user) == False
    assert organization.can_create(user) == False

    assert project.can_invite(user) == False
    assert project.can_create(user) == False
    assert project.can_manage(user) == False

    assert document.can_create(user) == True
    assert document.can_invite(user) == False
    assert document.can_manage(user) == False

    document.delete_create(user)
    document.add_invite(user)
    assert document.can_create(user) == True
    assert document.can_invite(user) == True
    assert document.can_manage(user) == False

    document.delete_invite(user)
    document.add_manage(user)
    assert document.can_create(user) == True
    assert document.can_invite(user) == True
    assert document.can_manage(user) == True
