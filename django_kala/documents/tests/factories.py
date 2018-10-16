import factory

from documents.models import Document, DocumentVersion


class DocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Document
        django_get_or_create = ('name', )

    name = factory.Faker('text')


class DocumentVersionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DocumentVersion
        django_get_or_create = ('name', )

    name = factory.Faker('text')
