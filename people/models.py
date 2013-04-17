from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django_localflavor_us.models import PhoneNumberField
from timezone_field import TimeZoneField
from kala.managers import ActiveManager
import companies
import projects


#should probably use AbstractBaseUser as the 30 char limit on users names is difficult.
class People(AbstractUser):
    title = models.CharField(max_length=255, null=True, blank=True)
    company = models.ForeignKey('companies.Companies')
    timezone = TimeZoneField(default=settings.TIME_ZONE, blank=True)
    access_new_projects = models.BooleanField()

    is_admin = models.BooleanField(default=False)

    # Phone numbers
    fax = PhoneNumberField(null=True, blank=True)
    home = PhoneNumberField(null=True, blank=True)
    mobile = PhoneNumberField(null=True, blank=True)
    office = PhoneNumberField(null=True, blank=True)
    ext = models.CharField(max_length=10, null=True, blank=True)

    last_updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    objects = UserManager()
    active = ActiveManager()

    class Meta:
        ordering = ['first_name', 'last_name']

    def set_active(self, active):
        self.is_active = active
        self.save()

    def get_companies_list(self):
        if self.is_admin:
            _companies = companies.models.Companies.active.all()
        else:
            _companies = companies.models.Companies.active.filter(
                pk__in=projects.models.Projects.clients.through.objects.filter(people__pk=self.pk).values(
                    'projects__company__pk'))
        has_projects = companies.models.Companies.active.filter(
            pk__in=projects.models.Projects.active.all().values('company__pk'))
        return _companies & has_projects
