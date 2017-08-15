from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_localflavor_us.models import PhoneNumberField
from timezone_field import TimeZoneField
from uuid import uuid4

import organizations
import projects
import datetime


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    uuid = models.UUIDField(unique=True, db_index=True, default=uuid4)
    title = models.CharField(max_length=255, null=True, blank=True)
    organizations = models.ManyToManyField('organizations.Organization')
    timezone = TimeZoneField(default=settings.TIME_ZONE, blank=True)
    access_new_projects = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)

    # Phone numbers
    fax = PhoneNumberField(null=True, blank=True)
    home = PhoneNumberField(null=True, blank=True)
    mobile = PhoneNumberField(null=True, blank=True)
    office = PhoneNumberField(null=True, blank=True)
    ext = models.CharField(max_length=10, null=True, blank=True)

    last_updated = models.DateTimeField(auto_now=True)
    removed = models.DateField(null=True)
    avatar_url = models.URLField(max_length=1200)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['first_name', 'last_name']
        db_table = 'kala_person'

    def set_active(self, active):
        self.is_active = active
        if not self.is_active:
            self.removed = datetime.date.today()
        self.save()

    def get_organizations(self, has_projects=True):
        if self.is_admin:
            _organizations = organizations.models.Organization.objects.active()
        else:
            _organizations = organizations.models.Organization.objects.active().filter(
                pk__in=projects.models.Project.clients.through.objects.filter(
                    user__pk=self.pk
                ).values('project__organization__pk')
            )
        if has_projects:
            has_projects = organizations.models.Organization.objects.active().filter(
                pk__in=projects.models.Project.objects.active().values('organization__pk'))
            return _organizations & has_projects
        return _organizations

    def get_projects(self):
        if self.is_admin:
            return projects.models.Project.objects.active()
        else:
            return projects.models.Project.objects.active().filter(
                organization__id=self.get_organizations().values_list('organization__pk')
            )

    def get_users(self):
        if self.is_admin:
            return User.objects.all()
        else:
            organizations = self.get_organizations().values_list('pk')
            return User.objects.filter(organizations__in=organizations)

    def send_invite(self):
        pass

    def __str__(self):  # pragma: no cover
        return "{0} {1}".format(self.first_name, self.last_name)
