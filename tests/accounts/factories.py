from kala.accounts.models import Person
from ..companies.factories import CompanyFactory
import factory


class PersonFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Person
    username = factory.Sequence(lambda n: 'user{0}'.format(n))
    company = factory.SubFactory(CompanyFactory)
    email = factory.LazyAttribute(lambda a: 'user.{0}@example.com'.format(a.username).lower())
    first_name = 'test'
    last_name = 'user'
    access_new_projects = True
