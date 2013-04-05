from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_localflavor_us.models import USPostalCodeField, USStateField, PhoneNumberField
from django_countries import CountryField
from timezone_field import TimeZoneField
from uuidfield import UUIDField


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = USStateField(null=True, blank=True)
    zip = USPostalCodeField(null=True, blank=True)
    country = CountryField(null=True, blank=True)
    fax = PhoneNumberField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    locale = models.CharField(max_length=2, null=True, blank=True)
    timezone = TimeZoneField(default='Pacific/Honolulu')
    website = models.URLField(null=True, blank=True)

    # remove when done
    bc_id = models.IntegerField()

    class Meta:
        ordering = ['name']

    def get_project_list(self):
        return Project.objects.filter(owner=self)

    def get_people_list(self):
        return Person.objects.filter(company=self)

    def __str__(self):
        return self.name


class Document(models.Model):
    project = models.ForeignKey('Project')
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def get_latest(self):
        return DocumentVersion.objects.filter(document=self).latest()

    def list_versions(self):
        return DocumentVersion.objects.filter(document=self).exclude(pk=self.get_latest().pk)


class DocumentVersion(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    document = models.ForeignKey('Document', null=True)
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True, auto_now_add=True)
    file = models.FileField(upload_to='/documents/', null=True, blank=True)
    mime = models.CharField(max_length=255, null=True)

    bc_latest = models.BooleanField()
    bc_size = models.IntegerField()
    bc_collection = models.IntegerField()
    bc_id = models.IntegerField()
    person = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    bc_project = models.ForeignKey('Project')
    bc_category = models.IntegerField(null=True, blank=True)
    bc_url = models.URLField(max_length=400)
    name = models.CharField(max_length=255)

    class Meta:
        get_latest_by = 'changed'
        ordering = ['name', 'changed']

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.document.name = self.name
        self.document.save()
        super(DocumentVersion, self).save(force_insert, force_update, using, update_fields)

    def get_icon(self):
        extension = self.bc_url.split('/')[-1].split('.')[-1]
        return 'img/icons/%s/%s-sm-32_32.png' % (extension, extension)

    def __str__(self):
        return self.name

#should probably use AbstractBaseUser as the 30 char limit on users names is difficult.
class Person(AbstractUser):
    title = models.CharField(max_length=255, null=True, blank=True)
    company = models.ForeignKey('Company')
    timezone = TimeZoneField(default='Pacific/Honolulu')
    access_new_projects = models.BooleanField()

    # ADD is_admin = models.BooleanField(default=False)

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
    bc_id = models.IntegerField(null=True, blank=True)


class Project(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey('Company', related_name='owner')
    additional_companies = models.ManyToManyField('Company', null=True, blank=True)
    clients = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True)

    bc_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True, auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

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
