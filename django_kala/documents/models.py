from django.conf import settings
from django.db import models
from django.http import HttpResponse
from django.utils import timezone
from uuid import uuid4
from managers import ActiveManager
from .defs import get_icon_for_mime, get_alt_for_mime


class Document(models.Model):
    project = models.ForeignKey('projects.Project')
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    removed = models.DateField(null=True)
    mime = models.CharField(max_length=255, null=True)
    category = models.ForeignKey('projects.Category', null=True)
    is_active = models.BooleanField(default=True)

    objects = ActiveManager()

    class Meta:
        ordering = ['-date', 'name']
        db_table = 'kala_documents'

    def set_active(self, active):
        self.is_active = active
        if not self.is_active:
            self.removed = timezone.now().date()
        self.save()

    def delete(self, using=None):
        DocumentVersion.objects.filter(document=self).delete()
        super(Document, self).delete(using)

    @property
    def uuid(self):
        if not hasattr(self, 'document'):
            self.document = self.get_latest()
        return self.document.uuid

    @property
    def description(self):
        if not hasattr(self, 'document'):
            self.document = self.get_latest()
        return self.document.description

    @property
    def person(self):
        if not hasattr(self, 'document'):
            self.document = self.get_latest()
        return self.document.person

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
        return DocumentVersion.objects.filter(document=self).latest()

    def list_versions(self):
        return DocumentVersion.objects.filter(document=self).exclude(pk=self.get_latest().pk)

    def __str__(self):
        return self.name


class DocumentVersion(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    document = models.ForeignKey('Document', null=True)
    file = models.FileField(null=True)
    url = models.URLField(max_length=3000)
    size = models.IntegerField(default=0)
    description = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now) # Update save method
    changed = models.DateTimeField(default=timezone.now) # Update save method
    mime = models.CharField(max_length=255, null=True)
    person = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    name = models.CharField(max_length=255)

    class Meta:
        get_latest_by = 'created'
        ordering = ['name', 'created']
        db_table = 'kala_document_version'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, save_document=True):
        if save_document:
            self.document.name = self.name
            self.document.date = self.created
            self.document.mime = self.mime
            self.document.save()
        super(DocumentVersion, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None):
        if Document.objects.filter(pk=self.document.pk).count() < 1:
            self.document.delete()
        super(DocumentVersion, self).delete(using)

    def http_response(self):
        response = HttpResponse(self.file.read(), content_type=self.mime)
        response['Content-Length'] = self.file.size
        response['Content-Disposition'] = 'attachment; filename={0}'.format(self.name)
        response['Content-Type'] = self.mime
        return response

    def get_icon(self):
        return get_icon_for_mime(self.mime)

    def get_alt(self):
        return get_alt_for_mime(self.mime)

    def __str__(self):
        return self.name
