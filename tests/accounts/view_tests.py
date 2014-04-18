from django.test.client import Client
from django_nose import FastFixtureTestCase
from kala.accounts.views import *
from .factories import PersonFactory
from ..projects.factories import ProjectFactory


class NotLoggedInTests(FastFixtureTestCase):
    def setUp(self):
        self.client = Client()

    def edit_profile_not_logged_in_test(self):
        person = PersonFactory(is_active=True)
        response = self.client.get(reverse('edit_profile', args=[person.pk]))
        self.assertRedirects(response, reverse('login'), status_code=302, target_status_code=200)

        response = self.client.post(reverse('edit_profile', args=[person.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'), status_code=302, target_status_code=200)


class EditProfileViewTests(FastFixtureTestCase):
    def setUp(self):
        self.client = Client()
        self.person = PersonFactory(is_active=True)
        self.person.set_password('test')
        self.person.save()
        self.client = Client()
        self.client.login(username=self.person.username, password='test')

    def edit_profile_test(self):
        # Test editing a profile
        data = self.person.__dict__
        data['first_name'] = 'foo'
        response = self.client.post(reverse('edit_profile', args=[self.person.pk]), data=data)
        self.assertEqual(response.status_code, 302)
        person = Person.objects.get(pk=self.person.pk)
        self.assertEqual('foo', person.first_name)

    def get_test(self):
        # Test doing a get without and with admin rights.
        response = self.client.get(reverse('edit_profile', args=[self.person.pk]))
        self.assertEqual(response.status_code, 200)

        self.person.is_admin = True
        self.person.save()
        response = self.client.get(reverse('edit_profile', args=[self.person.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('permission_forms' in response.context)

    def get_no_self_not_admin_test(self):
        # Expect to fail chaning someone else when we do not have admin rights.
        person = PersonFactory(is_active=True)
        response = self.client.get(reverse('edit_profile', args=[person.pk]))
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    def toggle_admin_not_admin_test(self):
        person = PersonFactory(is_active=True)

        # This should fail because we do not have admin rights.
        response = self.client.post(reverse('edit_profile', args=[person.pk]), data={'toggle-admin': True})
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

        self.person.is_admin = True
        self.person.save()
        # Now that we are admin, toggle the user admin flag.
        response = self.client.post(reverse('edit_profile', args=[person.pk]), data={'toggle-admin': True})
        self.assertRedirects(response, reverse('edit_profile', args=[person.pk]), status_code=302,
                             target_status_code=200)
        person = Person.objects.get(pk=person.pk)
        self.assertTrue(person.is_admin)

        # Toggle back to not admin
        response = self.client.post(reverse('edit_profile', args=[person.pk]), data={'toggle-admin': True})
        self.assertRedirects(response, reverse('edit_profile', args=[person.pk]), status_code=302,
                             target_status_code=200)
        person = Person.objects.get(pk=person.pk)
        self.assertFalse(person.is_admin)

    def toggle_admin_test(self):
        person = PersonFactory(is_active=True)

        # This should fail because we do not have admin rights.
        response = self.client.post(reverse('edit_profile', args=[person.pk]), data={'toggle-admin': True})
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

        self.person.is_admin = True
        self.person.save()
        # Now that we are admin, delete the user.
        response = self.client.post(reverse('edit_profile', args=[person.pk]), data={'delete': True})
        self.assertRedirects(response, reverse('accounts'), status_code=302,
                             target_status_code=200)
        person = Person.objects.get(pk=person.pk)
        self.assertFalse(person.is_active)

    def toggle_permissions_test(self):
        # We need to be admin to change permissions
        self.person.is_admin = True
        self.person.save()
        project = ProjectFactory(company=self.person.company)

#        raise Exception(str(permission_forms[0]['{0}'.format(project.pk)]))
        self.person.is_admin = True
        self.person.save()
        # Now that we are admin, delete the user.
        response = self.client.post(reverse('edit_profile', args=[self.person.pk]), data={'{0}'.format(project.pk):
                                                                                         'checked',
                                                                                          'save-permissions': True})
        self.assertRedirects(response, reverse('edit_profile', args=[self.person.pk]), status_code=302,
                             target_status_code=200)
        client = project.clients.get(pk=self.person.pk)
        self.assertEqual(client, self.person)

        # Remove from project and make sure there is no one there.
        response = self.client.post(reverse('edit_profile', args=[self.person.pk]), data={'save-permissions': True})
        self.assertRedirects(response, reverse('edit_profile', args=[self.person.pk]), status_code=302,
                             target_status_code=200)
        self.assertFalse(project.clients.all().exists())


class PeopleViewTests(FastFixtureTestCase):
    def setUp(self):
        self.client = Client()
        self.person = PersonFactory(is_active=True)
        self.person.set_password('test')
        self.person.save()
        self.client = Client()
        self.client.login(username=self.person.username, password='test')

    def not_admin_test(self):
        response = self.client.get(reverse('accounts'))
        self.assertTrue('companies' in response.context)
        self.assertFalse('person_form' in response.context)
        response = self.client.post(reverse('accounts'))
        self.assertRedirects(response, reverse('accounts'), status_code=302, target_status_code=200)

    def is_admin_test(self):
        self.person.is_admin = True
        self.person.save()
        response = self.client.get(reverse('accounts'))
        self.assertTrue('companies' in response.context)
        self.assertTrue('person_form' in response.context)

    def create_company_test(self):
        self.person.is_admin = True
        self.person.save()
        response = self.client.post(reverse('accounts'), data={'create_company': True, 'name': 'foo-bar'})
        company = Company.objects.get(name='foo-bar')
        self.assertTrue(company)
        self.assertRedirects(response, reverse('company', args=[company.pk]), status_code=302, target_status_code=200)

    def create_person_test(self):
        self.person.is_admin = True
        self.person.save()
        response = self.client.post(reverse('accounts'), data={'create_person': True, 'first_name': 'foo',
                                                               'last_name': 'bar', 'username': 'foobar',
                                                               'email': 'foo@bar.com', 'access_new_projects': 'checked',
                                                               'company': self.person.company.pk})
        person = Person.objects.get(email='foo@bar.com')
        self.assertTrue(person)
        self.assertRedirects(response, reverse('accounts'), status_code=302, target_status_code=200)

    def undelete_company_test(self):
        self.person.is_admin = True
        self.person.save()
        self.person.company.set_active(False)
        response = self.client.post(reverse('accounts'), data={'undelete': True, 'company': self.person.company.pk})
        self.assertTrue(Company.objects.get(pk=self.person.company.pk).is_active)
        self.assertRedirects(response, reverse('accounts'), status_code=302, target_status_code=200)

    def post_render_test(self):
        self.person.is_admin = True
        self.person.save()
        response = self.client.post(reverse('accounts'))
        self.assertTrue(response.status_code, 200)
