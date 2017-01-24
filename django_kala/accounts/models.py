from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django_localflavor_us.models import PhoneNumberField
from timezone_field import TimeZoneField
import companies
import projects
import datetime


class Person(AbstractUser):
    title = models.CharField(max_length=255, null=True, blank=True)
    company = models.ForeignKey('companies.Company')
    timezone = TimeZoneField(default=settings.TIME_ZONE, blank=True)
    access_new_projects = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)

    # Phone numbers
    fax = PhoneNumberField(null=True, blank=True)
    home = PhoneNumberField(null=True, blank=True)
    mobile = PhoneNumberField(null=True, blank=True)
    office = PhoneNumberField(null=True, blank=True)
    ext = models.CharField(max_length=10, null=True, blank=True)

    last_updated = models.DateTimeField(auto_now=True, auto_now_add=True)
    removed = models.DateField(null=True)

    objects = UserManager()

    class Meta:
        ordering = ['first_name', 'last_name']
        db_table = 'kala_person'

    def set_active(self, active):
        self.is_active = active
        if not self.is_active:
            self.removed = datetime.date.today()
        self.save()

    def get_companies(self):
        if self.is_admin:
            _companies = companies.models.Company.objects.active()
        else:
            _companies = companies.models.Company.objects.active().filter(
                pk__in=projects.models.Project.clients.through.objects.filter(person__pk=self.pk).values(
                    'project__company__pk'))
        has_projects = companies.models.Company.objects.active().filter(
            pk__in=projects.models.Project.objects.active().values('company__pk'))
        return _companies & has_projects

    def __str__(self):  # pragma: no cover
        return "{0} {1}".format(self.first_name, self.last_name)
