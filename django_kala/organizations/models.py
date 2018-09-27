from django.contrib.auth import get_user_model
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

    def get_people(self, user):
        # If you are a super user or you have permissions on
        # an organization, then you can see everyone.
        if user.is_superuser or Permissions.has_perms([
            'change_organization',
            'add_organization',
            'delete_organization'
        ], user, self.uuid):
            return User.objects.all()
        # TODO: This is a little to restrictive, but I think it needs some thinking about what should happen.
        else:
            return None

    def __str__(self):
        return self.name

    def can(self, user, _permissions):
        if user.is_superuser:
            return True
        # SELECT permission_id,
        #        user_id,
        #        object_uuid
        # FROM   kala_auth_permissions
        # WHERE  permission_id IN (SELECT auth_permission.id
        #                          FROM   auth_permission
        #                                 JOIN django_content_type
        #                                   ON auth_permission.content_type_id =
        #                                      django_content_type.id
        #                          WHERE  codename IN ( {0} )
        #                                 AND app_label = '{1}')
        #        AND user_id = {2}
        #        AND object_uuid = '{3}'.format((', '.join('"' + permission + '"' for permission in _permissions), 'organizations', user.id, str(self.uuid));
        permissions = Permission.objects.filter(codename__in=_permissions, content_type__app_label='organizations')
        Permissions.objects.filter(permission__in=permissions, user=user, object_uuid=self.uuid).exists()
        from django.db import connection
        print(connection.queries)
        if Permissions.objects.filter(permission__in=permissions, user=user, object_uuid=self.uuid).exists():
            return True
        return False

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
        Permissions.objects.get_or_create(
            permission=Permission.objects.get(
                codename=permission,
                content_type__app_label='organizations'
            ),
            user=user,
            object_uuid=self.uuid
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
            Permissions.objects.get(
                permission=Permission.objects.get(
                    codename=permission,
                    content_type__app_label='organizations'
                ),
                user=user,
                object_uuid=self.uuid
            ).delete()
        except Permissions.DoesNotExist:
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
