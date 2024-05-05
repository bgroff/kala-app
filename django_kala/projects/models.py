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
    id = models.AutoField(primary_key=True)
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
            return self.document_set.active().filter(project=self)
        return self.document_set.active().filter(
            project=self,
            id__in=user.get_documents().values_list('id', flat=True)
        )

    def can(self, user, _permissions):
        if user.is_superuser:
            return True

        return True if ProjectPermission.objects.filter(
            permission__in=Permission.objects.filter(
                codename__in=_permissions,
                content_type__app_label='projects'
            ),
            user=user,
            project=self).exists() or self.organization.can(user, _permissions) else False

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
        permission = Permission.objects.get(
            codename=permission,
            content_type__app_label='projects'
        )

        try:
            project_permission = ProjectPermission.objects.get(
                user=user,
                project=self
            )
            project_permission.permission = permission
            project_permission.save()
        except ProjectPermission.DoesNotExist:
            project_permission = ProjectPermission.objects.create(
                user=user,
                project=self,
                permission=permission
            )
        return project_permission

    def add_create(self, user):
        return self.add_permission(
            user,
            'can_create'
        )

    def add_invite(self, user):
        return self.add_permission(
            user,
            'can_invite'
        )

    def add_manage(self, user):
        return self.add_permission(
            user,
            'can_manage'
        )

    def delete_permission(self, user, permission):
        try:
            ProjectPermission.objects.get(
                permission=Permission.objects.get(
                    codename=permission,
                    content_type__app_label='projects'
                ),
                user=user,
                project=self
            ).delete()
        except ProjectPermission.DoesNotExist:
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


class ProjectPermission(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self): # pragma: no cover
        return '{0} | {1} | {2}'.format(self.project, self.user, self.permission.codename)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return '{0}'.format(self.name)


class Export(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    details = models.JSONField(default=dict)
