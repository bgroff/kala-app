from auth.models import Permissions
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django_kala.managers import ActiveManager
from taggit.managers import TaggableManager
from uuid import uuid4

import datetime

User = get_user_model()


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    tags = TaggableManager(blank=True)

    organization = models.ForeignKey('organizations.Organization')
    clients = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    removed = models.DateField(null=True)
    changed = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid4, editable=False)

    objects = ActiveManager()

    class Meta:
        ordering = ('name',)
        db_table = 'kala_projects'

    def set_active(self, active):
        self.is_active = active
        if not self.is_active:
            self.removed = datetime.date.today()
        self.save()

    def __str__(self):
        return self.name

    def get_documents(self, user):
        if user.is_superuser:
            return self.document_set.filter(project=self)
        if Permissions.has_perms([
            'change_organization',
            'add_organization',
            'delete_organization'
        ], user, self.organization.uuid) or Permissions.has_perms([
            'change_project',
            'add_project',
            'delete_project'
        ], user, self.uuid):
            return self.document_set.all().prefetch_related('documentversion_set', 'documentversion_set__user')
        else:
            document__uuids = self.document_set.all().values_list('uuid', flat=True)
            perm_uuids = Permissions.objects.filter(
                user=user,
                object_uuid__in=document__uuids
            ).values_list('object_uuid', flat=True)
            return self.document_set.filter(uuid__in=perm_uuids).prefetch_related('documentversion_set',
                                                                                  'documentversion_set__user')

    def get_users(self, user):
        if user.is_superuser:
            return User.objects.all()
        # If you have permissions for the org, or permissions for the
        # project, then you can see everyone in the org.
        if Permissions.has_perms([
            'change_organization',
            'add_organization',
            'delete_organization'
        ], user, self.organization.uuid) or Permissions.has_perms([
            'change_project',
            'delete_project'
        ], user, self.uuid):
            return self.organization.user_set.all()
        return None

    def add_change(self, user):
        perm = Permission.objects.get(codename='change_project')
        Permissions.add_perm(perm=perm, user=user, uuid=self.uuid)

    def has_change(self, user):
        perm = Permission.objects.get(codename='change_project')
        org_perm = Permission.objects.get(codename='change_organization')
        return Permissions.has_perm(
            perm=perm,
            user=user,
            uuid=self.uuid
        ) or Permissions.has_perm(
            perm=org_perm,
            user=user,
            uuid=self.organization.uuid
        )

    def add_delete(self, user):
        perm = Permission.objects.get(codename='delete_project')
        Permissions.add_perm(perm=perm, user=user, uuid=self.uuid)

    def has_delete(self, user):
        perm = Permission.objects.get(codename='delete_project')
        org_perm = Permission.objects.get(codename='delete_organization')
        return Permissions.has_perm(
            perm=perm,
            user=user,
            uuid=self.uuid
        ) or Permissions.has_perm(
            perm=org_perm,
            user=user,
            uuid=self.organization.uuid
        )

    def add_create(self, user):
        perm = Permission.objects.get(codename='add_project')
        Permissions.add_perm(perm=perm, user=user, uuid=self.uuid)

    def has_create(self, user):
        perm = Permission.objects.get(codename='add_project')
        org_perm = Permission.objects.get(codename='add_organization')
        return Permissions.has_perm(
            perm=perm,
            user=user,
            uuid=self.uuid
        ) or Permissions.has_perm(
            perm=org_perm,
            user=user,
            uuid=self.organization.uuid
        )


class Category(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project)
    type = models.CharField(max_length=20, db_index=True, null=True, blank=True)

    def __str__(self):
        return '{0}'.format(self.name)
