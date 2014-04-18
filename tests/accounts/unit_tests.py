from django_nose import FastFixtureTestCase
from .factories import PersonFactory
from ..projects.factories import ProjectFactory
import datetime


class PersonTests(FastFixtureTestCase):
    def setUp(self):
        self.person = PersonFactory(username='test_user')

    def full_name_test(self):
        self.assertEqual('test user', self.person.get_full_name())

    def short_name_test(self):
        self.assertEqual('test', self.person.get_short_name())

    def username_test(self):
        self.assertEqual('test_user', self.person.get_username())

    def set_active_test(self):
        self.person.set_active(False)
        self.assertFalse(self.person.is_active)
        self.assertEqual(datetime.date.today(), self.person.removed)
        self.person.set_active(True)
        self.assertTrue(self.person.is_active)

    def get_companies_test(self):
        # The company does not have any projects at the moment, so we do not show it.
        self.assertEqual(0, self.person.get_companies().count())

        # Add a project and make this person a client.
        project = ProjectFactory(company=self.person.company)
        project.clients.add(self.person)
        self.assertEqual(1, self.person.get_companies().count())

        # Add a project with no one in it. This will also create a new company
        ProjectFactory()
        self.assertEqual(1, self.person.get_companies().count())

        # Test that as an admin we get all the companies no matter what.
        self.person.is_admin = True
        self.person.save()
        self.assertEqual(2, self.person.get_companies().count())

    def str_test(self):
        self.assertEqual(str(self.person), "{0} {1}".format(self.person.first_name, self.person.last_name))
