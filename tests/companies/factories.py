from kala.companies.models import Company
import factory


class CompanyFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Company
    name = factory.Sequence(lambda n: 'company-{0}'.format(n))
