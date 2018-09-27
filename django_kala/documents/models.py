from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db import models
from django.shortcuts import redirect
from django.utils import timezone
from uuid import uuid4
from taggit.managers import TaggableManager

from auth.models import Permissions
from django_kala.managers import ActiveManager
from .defs import get_icon_for_mime, get_alt_for_mime

User = get_user_model()


class Document(models.Model):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    removed = models.DateField(null=True)
    mime = models.CharField(max_length=255, null=True)
    category = models.ForeignKey('projects.Category', null=True, blank=True, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid4, editable=False)

    tags = TaggableManager(blank=True)
    objects = ActiveManager()

    class Meta:
        ordering = ['-date', 'name']
        db_table = 'kala_documents'

    def set_active(self, active):
        manager = settings.PLATFORM_MANAGER()
        manager.archive_document(self) if active else manager.retrieve_document(self)

        self.is_active = active
        if not self.is_active:
            self.removed = timezone.now().date()
        self.save()

    def delete(self, using=None, **kwargs):
        DocumentVersion.objects.filter(document=self).delete()
        super(Document, self).delete(using)

    @property
    def description(self):
        if not hasattr(self, 'document'):
            self.document = self.get_latest()
        return self.document.description

    @property
    def user(self):
        if not hasattr(self, 'document'):
            self.document = self.get_latest()
        return self.document.user

    @property
    def created(self):
        if not hasattr(self, 'document'):
            self.document = self.get_latest()
        return self.document.created

    @property
    def file(self):
        if not hasattr(self, 'document'):
            self.document = self.get_latest()
        return self.document.file

    @property
    def get_icon(self):
        if not hasattr(self, 'document'):
            self.document = self.get_latest()
        return self.document.get_icon()

    @property
    def get_alt(self):
        if not hasattr(self, 'document'):
            self.document = self.get_latest()
        return self.document.get_alt()

    def get_latest(self):
        return self.documentversion_set.latest()

    def list_versions(self):
        return self.documentversion_set.all()

    def get_users(self, user):
        if user.is_superuser:
            return User.objects.all()
        # If you have permissions for the org, or permissions for the
        # project, then you can see everyone in the org.
        if Permissions.has_perms([
            'change_organization',
            'add_organization',
            'delete_organization'
        ], user, self.project.organization.uuid) or Permissions.has_perms([
            'add_project',
            'change_project',
            'delete_project'
        ], user, self.project.uuid):
            return self.project.organization.user_set.all()
        if Permissions.has_perms([
            'add_document',
            'change_document',
            'delete_document'
        ], user, self.uuid):
            project_users = DocumentVersion.objects.filter(
                document__project=self.project
            ).prefetch_related(
                'document_set'
            ).select_related(
                'user_id'
            ).values_list(
                'user_id', flat=True
            )
            return User.objects.filter(id__in=project_users)
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
        permissions = Permission.objects.filter(codename__in=_permissions, content_type__app_label='organizations')
        Permissions.objects.filter(permission__in=permissions, user=user, object_uuid=self.uuid).exists()
        from django.db import connection
        print(connection.queries)
        if Permissions.objects.filter(permission__in=permissions, user=user, object_uuid=self.uuid).exists() \
                or self.project.can(user, _permissions) \
                or self.project.organization.can(user, _permissions):
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
                content_type__app_label='documents'
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
                    content_type__app_label='documents'
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

    def __str__(self):
        return self.name


class DocumentVersion(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    document = models.ForeignKey('Document', null=True, on_delete=models.CASCADE)
    # This is so that the bc api can create documents without getting the file.
    file = models.FileField(null=True, max_length=255)
    url = models.URLField(max_length=3000)
    size = models.IntegerField(default=0)
    description = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now) # Update save method
    changed = models.DateTimeField(default=timezone.now) # Update save method
    mime = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)

    class Meta:
        get_latest_by = 'created'
        ordering = ['name', 'created']
        db_table = 'kala_document_version'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, save_document=False):
        if save_document:
            self.document.mime = self.mime
            self.document.save()
        super(DocumentVersion, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None):
        if Document.objects.filter(pk=self.document.pk).count() < 1:
            self.document.delete()
        super(DocumentVersion, self).delete(using)

    def http_response(self):
        manager = settings.PLATFORM_MANAGER()
        url = manager.get_document_url(self)
        return redirect(url)

    def get_icon(self):
        return get_icon_for_mime(self.mime)

    def get_alt(self):
        return get_alt_for_mime(self.mime)

    def __str__(self):
        return self.name
