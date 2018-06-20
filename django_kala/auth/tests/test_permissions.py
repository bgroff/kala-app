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
    organization.add_change(user)
    project = ProjectFactory.create(organization=organization)
    document = DocumentFactory.create(project=project)

    assert len(user.get_organizations()) == 1
    assert len(user.get_projects()) == 1
    assert len(user.get_documents()) == 1

    assert organization.has_change(user) == True
    assert organization.has_delete(user) == False
    assert organization.has_create(user) == False

    assert project.has_delete(user) == False
    assert project.has_create(user) == False
    assert project.has_change(user) == True

    assert document.has_delete(user) == False
    assert document.has_create(user) == False
    assert document.has_change(user) == True

    organization.add_delete(user)

    assert project.has_delete(user) == True
    assert project.has_create(user) == False
    assert project.has_change(user) == True

    assert document.has_delete(user) == True
    assert document.has_create(user) == False
    assert document.has_change(user) == True

    organization.add_create(user)

    assert project.has_delete(user) == True
    assert project.has_create(user) == True
    assert project.has_change(user) == True

    assert document.has_delete(user) == True
    assert document.has_create(user) == True
    assert document.has_change(user) == True



@pytest.mark.django_db
def test_user_has_project_permissions():
    user = UserFactory.create()

    organization = OrganizationFactory.create()
    project = ProjectFactory.create(organization=organization)
    project.add_change(user)
    document = DocumentFactory.create(project=project)

    assert len(user.get_organizations()) == 1
    assert len(user.get_projects()) == 1
    assert len(user.get_documents()) == 1
    assert organization.has_change(user) == False
    assert organization.has_delete(user) == False
    assert organization.has_create(user) == False

    assert project.has_delete(user) == False
    assert project.has_create(user) == False
    assert project.has_change(user) == True

    assert document.has_delete(user) == False
    assert document.has_create(user) == False
    assert document.has_change(user) == True

    project.add_delete(user)
    assert project.has_delete(user) == True

    assert document.has_delete(user) == True
    assert document.has_create(user) == False
    assert document.has_change(user) == True

    project.add_create(user)
    assert project.has_create(user) == True

    assert document.has_delete(user) == True
    assert document.has_create(user) == True
    assert document.has_change(user) == True


@pytest.mark.django_db
def test_user_has_document_permissions():
    user = UserFactory.create()

    organization = OrganizationFactory.create()
    project = ProjectFactory.create(organization=organization)
    document = DocumentFactory.create(project=project)
    document.add_change(user)

    assert len(user.get_organizations()) == 1
    assert len(user.get_projects()) == 1
    assert len(user.get_documents()) == 1
    assert organization.has_change(user) == False
    assert organization.has_delete(user) == False
    assert organization.has_create(user) == False

    assert project.has_delete(user) == False
    assert project.has_create(user) == False
    assert project.has_change(user) == False

    assert document.has_delete(user) == False
    assert document.has_create(user) == False
    assert document.has_change(user) == True

    document.add_delete(user)
    assert document.has_delete(user) == True

    document.add_create(user)
    assert document.has_create(user) == True
