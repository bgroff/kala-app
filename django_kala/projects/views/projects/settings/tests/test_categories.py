import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND

from projects.models import Category
from projects.views.projects.tests import setup, login, user_permissions_test_manage


@pytest.mark.django_db
def test_user_permissions_for_project_categories():
    user, organization, project, client = setup()
    user_permissions_test_manage(
        view='projects:categories',
        client=client,
        user=user,
        organization=organization,
        project=project,
        args=[project.pk]
    )


@pytest.mark.django_db
def test_user_permissions_for_deleting_project_category():
    user, organization, project, client = setup()
    category = Category.objects.create(name='Test Category', project=project)
    user_permissions_test_manage(
        view='projects:delete_category',
        client=client,
        user=user,
        organization=organization,
        project=project,
        args=[project.pk, category.pk]
    )


@pytest.mark.django_db
def test_user_permissions_for_creating_project_category():
    user, organization, project, client = setup()
    user_permissions_test_manage(
        view='projects:new_category',
        client=client,
        user=user,
        organization=organization,
        project=project,
        args=[project.pk]
    )


@pytest.mark.django_db
def test_user_permissions_for_editing_project_category():
    user, organization, project, client = setup()
    category = Category.objects.create(name='Test Category', project=project)
    user_permissions_test_manage(
        view='projects:edit_category',
        client=client,
        user=user,
        organization=organization,
        project=project,
        args=[project.pk, category.pk]
    )


@pytest.mark.django_db
def test_editing_project_category():
    user, organization, project, client = setup()
    project.add_manage(user)
    assert login(client, user)

    category = Category.objects.create(name='Test Category', project=project)
    response = client.post(
        path=reverse('projects:edit_category', args=[project.pk, category.pk]),
        data={
            'name': 'Another Name',
        },
        follow=True
    )

    assert response.redirect_chain[0][0] == reverse('projects:edit_category', args=[project.pk, category.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND

    category.refresh_from_db()
    assert category.name == 'Another Name'

    # Bad data
    response = client.post(
        path=reverse('projects:edit_category', args=[project.pk, category.pk]),
        data={
            'foo': 'bar',
        },
        follow=True
    )

    assert response.status_code == HTTP_200_OK
    category.refresh_from_db()
    assert category.name == 'Another Name'


@pytest.mark.django_db
def test_creating_project_category():
    user, organization, project, client = setup()
    project.add_manage(user)
    assert login(client, user)

    assert len(project.category_set.all()) == 0
    response = client.post(
        path=reverse('projects:new_category', args=[project.pk]),
        data={
            'name': 'Test Category',
        },
        follow=True
    )

    assert response.redirect_chain[0][0] == reverse('projects:categories', args=[project.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    assert len(project.category_set.all()) == 1
    assert project.category_set.first().name == 'Test Category'

    # Bad data
    response = client.post(
        path=reverse('projects:new_category', args=[project.pk]),
        data={
            'foo': 'bar',
        },
        follow=True
    )

    assert response.status_code == HTTP_200_OK
    assert len(project.category_set.all()) == 1
    assert project.category_set.first().name == 'Test Category'


@pytest.mark.django_db
def test_deleting_project_category():
    user, organization, project, client = setup()
    project.add_manage(user)
    assert login(client, user)

    category = Category.objects.create(name='Test Category', project=project)
    assert len(project.category_set.all()) == 1
    response = client.delete(
        path=reverse('projects:delete_category', args=[project.pk, category.pk]),
        follow=True
    )

    assert response.redirect_chain[0][0] == reverse('projects:categories', args=[project.pk])
    assert response.redirect_chain[0][1] == HTTP_302_FOUND
    assert len(project.category_set.all()) == 0
