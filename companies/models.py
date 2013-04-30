from django.conf import settings
from django_localflavor_us.models import USPostalCodeField, PhoneNumberField
from django.db import models
from django_countries import CountryField
from django_localflavor_us.models import USStateField
from kala.managers import ActiveManager
from people.models import People
from projects.models import Projects
from timezone_field import TimeZoneField


class Companies(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = USStateField(null=True, blank=True)
    country = CountryField(default='US')
    fax = PhoneNumberField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    locale = models.CharField(max_length=2, null=True, blank=True, default='en')
    timezone = TimeZoneField(default=settings.TIME_ZONE)
    website = models.URLField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ['name']

    def __init__(self, *args, **kwargs):
        super(Companies, self).__init__(*args, **kwargs)
        self.__is_active = self.is_active

    def set_active(self, active):
        self.is_active = active
        for person in People.objects.filter(company=self):
            person.set_active(active)

        for project in Projects.objects.filter(company=self):
            project.set_active(active)

        self.save()

    def get_project_list(self, person):
        assert type(person) is People, 'The user parameter must be of type People'
        if person.is_admin:
            return Projects.active.filter(company=self)
        else:
            return Projects.active.filter(company=self,
                                          pk__in=Projects.clients.through.objects.filter(people=person).values(
                                              'projects__pk'))

    def get_people_list(self):
        return People.active.filter(company=self)

    def add_person_to_projects(self, person):
        assert type(person) is People, 'The person parameter must be of type People'
        for project in Projects.active.filter(company=self):
            project.clients.add(person)

    def __str__(self):
        return self.name
