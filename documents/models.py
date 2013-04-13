from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponse
from django_localflavor_us.models import USPostalCodeField, USStateField, PhoneNumberField
from django_countries import CountryField
from documents.defs import get_icon_for_mime
from timezone_field import TimeZoneField
from uuidfield import UUIDField


class ActiveManager(models.Manager):
    def get_query_set(self):
        return super(ActiveManager, self).get_query_set().filter(is_active=True)


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = USStateField(null=True, blank=True)
    zip = USPostalCodeField(null=True, blank=True)
    country = CountryField(default='US')
    fax = PhoneNumberField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    locale = models.CharField(max_length=2, null=True, blank=True)
    timezone = TimeZoneField(default=settings.TIME_ZONE)
    website = models.URLField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ['name']

    def __init__(self, *args, **kwargs):
        super(Company, self).__init__(*args, **kwargs)
        self.__is_active = self.is_active

    def set_active(self, active):
        self.is_active = active
        for person in Person.objects.filter(company=self):
            person.set_active(active)

        for project in Project.objects.filter(owner=self):
            project.set_active(active)

        self.save()

    def get_project_list(self, user):
        if user.is_admin:
            return Project.active.filter(owner=self)
        else:
            return Project.active.filter(owner=self, pk__in=Project.clients.through.active.filter(person=user).values(
                'project__pk'))

    def get_people_list(self):
        return Person.active.filter(company=self)

    def __str__(self):
        return self.name


class Document(models.Model):
    project = models.ForeignKey('Project')
    name = models.CharField(max_length=255)
    date = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ['-date', 'name']

    def set_active(self, active):
        self.is_active = active
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


# Document upload functions
def upload_document_to(instance, filename):
    """
    """
    return "%s%s" % (settings.DOCUMENT_ROOT, str(instance.pk))


class DocumentStorage(FileSystemStorage):
    """
    """
    def url(self, name):
        document = Document.objects.get(file=name)
        return unicode(reverse('download_document', args=[str(document.pk)]))
document_file_storage = DocumentStorage(location=settings.DOCUMENT_ROOT)


class DocumentVersion(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    document = models.ForeignKey('Document', null=True)
    file = models.FileField(upload_to=upload_document_to, storage=document_file_storage)
    description = models.TextField(null=True)
    created = models.DateTimeField() # Update save method
    changed = models.DateTimeField(auto_now=True) # Update save method
    mime = models.CharField(max_length=255, null=True)
    person = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    name = models.CharField(max_length=255)

    class Meta:
        get_latest_by = 'changed'
        ordering = ['name', 'changed']

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, save_document=True):
        if save_document:
            self.document.name = self.name
            self.document.save()
        super(DocumentVersion, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None):
        if Document.objects.filter(pk=self.document.pk).count() < 1:
            self.document.delete()
        super(DocumentVersion, self).delete(using)

    def build_http_response(self):
        response = HttpResponse(self.file.read(), mimetype=self.name)
        response['Content-Length'] = self.file.size
        response['Content-Disposition'] = 'attachment; filename=' + self.name
        response['Content-Type'] = self.mime
        return response

    def get_icon(self):
        return get_icon_for_mime(self.mime)

    def get_alt(self):
        extension = self.bc_url.split('/')[-1].split('.')[-1]
        if extension is 'doc' or 'docx': return 'Word Document'
        if extension is 'ppt' or 'pptx': return 'Power Point'
        if extension is 'pdf': return 'PDF Document'
        if extension is 'xls' or 'xlsx': return 'Excel Document'
        return 'Unkwown Document'

    def __str__(self):
        return self.name.encode('utf-8')


#should probably use AbstractBaseUser as the 30 char limit on users names is difficult.
class Person(AbstractUser):
    title = models.CharField(max_length=255, null=True, blank=True)
    company = models.ForeignKey('Company')
    timezone = TimeZoneField(default=settings.TIME_ZONE, blank=True)
    access_new_projects = models.BooleanField()

    is_admin = models.BooleanField(default=False)

    # Phone numbers
    fax = PhoneNumberField(null=True, blank=True)
    home = PhoneNumberField(null=True, blank=True)
    mobile = PhoneNumberField(null=True, blank=True)
    office = PhoneNumberField(null=True, blank=True)
    ext = models.CharField(max_length=10, null=True, blank=True)

    im_handle = models.CharField(max_length=255, null=True, blank=True)
    im_service = models.CharField(max_length=255, null=True, blank=True)

    last_updated = models.DateTimeField(auto_now=True, auto_now_add=True)
    avatar_url = models.URLField(null=True, blank=True, max_length=400)

    objects = UserManager()
    active = ActiveManager()

    class Meta:
        ordering = ['first_name', 'last_name']

    def set_active(self, active):
        self.is_active = active
        self.save()

    def get_companies_list(self):
        if self.is_admin:
            companies = Company.active.all()
        else:
            q1 = Company.objects.filter(
                pk__in=Project.clients.through.active.filter(person=self).values('project__owner__pk'))
            q2 = Company.active.filter(pk=self.company.pk)
            companies = q1 | q2
        has_projects = Company.active.filter(pk__in=Project.active.all().values('owner__pk'))
        return companies & has_projects


class Project(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey('Company', related_name='owner')
    additional_companies = models.ManyToManyField('Company', null=True, blank=True)
    clients = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True, auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveManager()

    def set_active(self, active):
        self.is_active = active
        for document in Document.objects.filter(project=self):
            document.set_active(active)
        self.save()

    def add_client(self, client):
        assert type(client) is Person, 'The parameter must be of type Person.'

        # Make sure that the clients company is in the list of additional companies
        try:
            self.additional_companies.get(client.company)
        except Company.DoesNotExist:
            self.additional_companies.add(client.company)

        # Otherwise check if the client is in the clients list, add if not.
        try:
            self.clients.get(client)
        except Person.DoesNotExist:
            self.clients.add(client)

    def remove_client(self, client):
        assert type(client) is Person, 'The parameter must be of type Person.'
        self.clients.remove(client)

    def add_company(self, company):
        assert type(company) is Company, 'The parameter must be of type Company.'

    def remove_company(self, company):
        assert type(company) is Person, 'The parameter must be of type Company.'

    def __str__(self):
        return self.name
