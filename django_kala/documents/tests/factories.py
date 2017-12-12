import factory

from documents.models import Document
from projects.tests.factories import ProjectFactory


class DocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Document
        django_get_or_create = ('name', )

    name = factory.Faker('text')
