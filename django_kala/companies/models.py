from django.conf import settings
from django.db import models
from django_countries.fields import CountryField
from django_localflavor_us.models import PhoneNumberField, USStateField
from timezone_field import TimeZoneField
from uuid import uuid4

from managers import ActiveManager
from projects.models import Project

import datetime


class CompaniesWithProjectManager(models.Manager):
    def get_query_set(self):
        return super(CompaniesWithProjectManager, self).get_query_set().filter(
            is_active=True,
            pk__in=Project.objects.active().values('company__pk')
        )


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid4)
    address = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = USStateField(null=True, blank=True)
    zip = models.CharField(max_length=25, null=True, blank=True)
    country = CountryField(default='US')
    fax = PhoneNumberField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    locale = models.CharField(max_length=2, null=True, blank=True, default='en')
    removed = models.DateField(null=True)
    timezone = TimeZoneField(default=settings.TIME_ZONE)
    website = models.URLField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    objects = ActiveManager()
    with_projects = CompaniesWithProjectManager()

    class Meta:
        ordering = ['name']
        db_table = 'kala_companies'

    def set_active(self, active):
        self.is_active = active
        for person in self.user_set.all():
            person.set_active(active)

        for project in Project.objects.filter(company=self):
            project.set_active(active)

        if not self.is_active:
            self.removed = datetime.date.today()
        self.save()

    def get_projects(self, person=None):
    #        assert type(person) is People, 'The user parameter must be of type People'
        if not person or person.is_admin:
            return Project.objects.active().filter(company=self)
        else:
            return Project.objects.active().filter(company=self,
                                                   pk__in=Project.clients.through.objects.filter(
                                                       person=person
                                                   ).values('project__pk'))

    def get_people(self):
        return self.user_set.all()  # Todo: only show people that are active

    def add_person_to_projects(self, person):
        for project in Project.active.filter(company=self):
            project.clients.add(person)

    def __str__(self):
        return self.name
