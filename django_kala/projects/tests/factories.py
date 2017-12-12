import factory

from projects.models import Project


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project
        django_get_or_create = ('name', )

    name = factory.Faker('text')
    description = factory.Faker('text')
