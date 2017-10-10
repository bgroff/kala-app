from django.conf import settings
from django.contrib.auth.models import Permission
from django.db import models
from django_localflavor_us.models import PhoneNumberField
from timezone_field import TimeZoneField
from uuid import uuid4

from auth.models import Permissions
from django_kala.managers import ActiveManager
from projects.models import Project

import documents
import datetime


class OrganizationsWithProjectManager(models.Manager):
    def get_query_set(self):
        return super(OrganizationsWithProjectManager, self).get_query_set().filter(
            is_active=True,
            pk__in=Project.objects.active().values('organization__pk')
        )


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid4)
    address = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(null=True, blank=True, max_length=80)
    zip = models.CharField(max_length=25, null=True, blank=True)
    country = models.CharField(default='US', null=True, blank=True, max_length=80)
    fax = PhoneNumberField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    locale = models.CharField(max_length=2, null=True, blank=True, default='en')
    removed = models.DateField(null=True)
    timezone = TimeZoneField(default=settings.TIME_ZONE)
    website = models.URLField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    objects = ActiveManager()
    with_projects = OrganizationsWithProjectManager()

    class Meta:
        ordering = ['name']
        db_table = 'kala_companies'

    def set_active(self, active):
        self.is_active = active
        for person in self.user_set.all():
            person.set_active(active)

        for project in Project.objects.filter(organization=self):
            project.set_active(active)

        if not self.is_active:
            self.removed = datetime.date.today()
        self.save()

    def get_projects(self, user):
        if user.is_superuser:
            return Project.objects.active().filter(organization=self)
        if Permissions.has_perms([
            'change_organization',
            'add_organization',
            'delete_organization'
        ], user, self.uuid):
            return self.project_set.all()
        else:
            document_project_uuids = Permissions.objects.filter(permission__codename__in=[
                'change_document',
                'add_document',
                'delete_document'
            ], user=user).values_list('object_uuid', flat=True)
            document_projects = documents.models.Document.objects.filter(
                project__organization=self,
                uuid__in=document_project_uuids
            ).values_list('project__uuid', flat=True)

            project__uuids = self.project_set.all().values_list('uuid', flat=True)
            perm_uuids = Permissions.objects.filter(
                user=user,
                object_uuid__in=project__uuids
            ).values_list('object_uuid', flat=True)
            return Project.objects.filter(uuid__in=list(perm_uuids) + list(document_projects))

    def get_people(self):
        return self.user_set.all()  # Todo: only show people that are active

    def add_person_to_projects(self, person):
        for project in Project.active.filter(organization=self):
            project.clients.add(person)

    def __str__(self):
        return self.name

    def add_read(self, user):
        perm = Permission.objects.get(codename='change_organization')
        Permissions.add_perm(perm=perm, user=user, uuid=self.uuid)

    def has_read(self, user):
        perm = Permission.objects.get(codename='change_organization')
        return Permissions.has_perm(perm=perm, user=user, uuid=self.uuid)

    def add_delete(self, user):
        perm = Permission.objects.get(codename='delete_organization')
        Permissions.add_perm(perm=perm, user=user, uuid=self.uuid)

    def has_delete(self, user):
        perm = Permission.objects.get(codename='delete_organization')
        return Permissions.has_perm(perm=perm, user=user, uuid=self.uuid)

    def add_create(self, user):
        perm = Permission.objects.get(codename='add_organization')
        Permissions.add_perm(perm=perm, user=user, uuid=self.uuid)

    def has_create(self, user):
        perm = Permission.objects.get(codename='add_organization')
        return Permissions.has_perm(perm=perm, user=user, uuid=self.uuid)
