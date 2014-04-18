from kala.projects.models import Project
from ..companies.factories import CompanyFactory
import factory


class ProjectFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Project
    name = factory.Sequence(lambda n: 'project-{0}'.format(n))
    company = factory.SubFactory(CompanyFactory)
