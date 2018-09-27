from django.contrib.postgres.fields import JSONField

from auth.models import Permissions
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
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

    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)
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
        permissions = Permission.objects.filter(codename__in=_permissions, content_type__app_label='projects')
        Permissions.objects.filter(permission__in=permissions, user=user, object_uuid=self.uuid).exists()
        from django.db import connection
        print(connection.queries)
        if Permissions.objects.filter(permission__in=permissions, user=user, object_uuid=self.uuid).exists() or self.organization.can(user, _permissions):
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
                content_type__app_label='projects'
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
                    content_type__app_label='projects'
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


class Category(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, db_index=True, null=True, blank=True)

    def __str__(self):
        return '{0}'.format(self.name)


class Export(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    details = JSONField(default={})
