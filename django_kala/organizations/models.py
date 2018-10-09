from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import Permission
from django.db import models
from django_localflavor_us.models import PhoneNumberField
from timezone_field import TimeZoneField
from uuid import uuid4

from django_kala.managers import ActiveManager
from projects.models import Project

import datetime

User = get_user_model()


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
    state = models.CharField(max_length=80, null=True, blank=True)
    zip = models.CharField(max_length=25, null=True, blank=True)
    country = models.CharField(max_length=80, null=True, blank=True, default='US')
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
        else:
            return Project.objects.filter(id__in=user.get_projects().values_list('id', flat=True), organization=self)

    def get_people(self, user):
        if user.is_superuser:
            return User.objects.all()
        else:
            return user.get_users()

    def __str__(self):
        return self.name

    def can(self, user, _permissions):
        if user.is_superuser:
            return True

        return True if OrganizationPermission.objects.filter(
            permission__in=Permission.objects.filter(
                codename__in=_permissions,
                content_type__app_label='organizations'
            ),
            user=user,
            organization=self
        ).exists() else False

    def can_create(self, user):
        return self.can(user, [
            'can_create',
            'can_invite',
            'can_manage'
        ])

    def can_invite(self, user):
        return self.can(user, [
            'can_invite',
            'can_manage'
        ])

    def can_manage(self, user):
        return self.can(user, [
            'can_manage'
        ])

    def add_permission(self, user, permission):
        OrganizationPermission.objects.get_or_create(
            permission=Permission.objects.get(
                codename=permission,
                content_type__app_label='organizations'
            ),
            user=user,
            organization=self
        )

    def add_create(self, user):
        self.add_permission(
            user,
            'can_create'
        )

    def add_invite(self, user):
        self.add_permission(
            user,
            'can_invite'
        )

    def add_manage(self, user):
        self.add_permission(
            user,
            'can_manage'
        )

    def delete_permission(self, user, permission):
        try:
            OrganizationPermission.objects.get(
                permission=Permission.objects.get(
                    codename=permission,
                    content_type__app_label='organizations'
                ),
                user=user,
                organization=self
            ).delete()
        except OrganizationPermission.DoesNotExist:
            return False

    def delete_create(self, user):
        self.delete_permission(
            user,
            'can_create'
        )

    def delete_invite(self, user):
        self.delete_permission(
            user,
            'can_invite'
        )

    def delete_manage(self, user):
        self.delete_permission(
            user,
            'can_manage'
        )


class OrganizationPermission(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} | {1} | {2}'.format(self.organization, self.user, self.permission.codename)
