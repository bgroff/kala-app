import datetime
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractUser, Permission
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import models
from django.template import loader
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from django_localflavor_us.models import PhoneNumberField
from timezone_field import TimeZoneField

import documents
import organizations
import projects


# TODO: This does not work.
class KalaUserManager(UserManager):

    def get_query_set(self):
        return super(KalaUserManager, self).get_query_set().filter(is_active=True)


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    uuid = models.UUIDField(unique=True, db_index=True, default=uuid4)
    title = models.CharField(max_length=255, null=True, blank=True)
    organizations = models.ManyToManyField('organizations.Organization')
    timezone = TimeZoneField(default=settings.TIME_ZONE, blank=True)
    access_new_projects = models.BooleanField(default=False)

    # Phone numbers
    fax = PhoneNumberField(null=True, blank=True)
    home = PhoneNumberField(null=True, blank=True)
    mobile = PhoneNumberField(null=True, blank=True)
    office = PhoneNumberField(null=True, blank=True)
    ext = models.CharField(max_length=10, null=True, blank=True)

    last_updated = models.DateTimeField(auto_now=True)
    removed = models.DateField(null=True)
    avatar_url = models.URLField(max_length=1200)

    objects = KalaUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['first_name', 'last_name']
        db_table = 'kala_user'

    def set_active(self, active):
        self.is_active = active
        if not self.is_active:
            self.removed = datetime.date.today()
        self.save()

    def get_organizations_with_create(self):
        if self.is_superuser:
            return organizations.models.Organization.objects.active()
        return organizations.models.Organization.objects.active().filter(
            id__in=organizations.models.OrganizationPermission.objects.filter(
                user=self
            ).values_list('organization__id', flat=True))

    def get_organizations(self, permission=None):
        if self.is_superuser:
            return organizations.models.Organization.objects.active()
        else:
            kwargs = {
                'user': self
            }
            if permission:
                kwargs['permission__codename__in'] = permission

            return organizations.models.Organization.objects.active().filter(
                id__in=set().union(*[
                    list(organizations.models.OrganizationPermission.objects.filter(**kwargs).values_list('organization__id', flat=True)),
                    list(projects.models.ProjectPermission.objects.filter(**kwargs).values_list('project__organization__id',flat=True).values_list('id',flat=True)),
                    list(documents.models.DocumentPermission.objects.filter(**kwargs).values_list('document__project__organization__id', flat=True))
                ])
            )

    def get_projects(self):
        if self.is_superuser:
            return projects.models.Project.objects.active()
        else:
            return projects.models.Project.objects.active().filter(
                id__in=set().union(*[
                    list(projects.models.ProjectPermission.objects.filter(user=self).values_list('project__id', flat=True)),
                    list(projects.models.Project.objects.filter(organization__id__in=organizations.models.OrganizationPermission.objects.filter(user=self).values_list('organization__id', flat=True)).values_list('id', flat=True)),
                    list(documents.models.DocumentPermission.objects.filter(user=self).values_list('document__project__id', flat=True))
                ])
            )

    def get_documents(self):
        if self.is_superuser:
            return documents.models.Document.objects.active()
        else:
            return documents.models.Document.objects.active().filter(
                id__in=set().union(*[
                    list(documents.models.DocumentPermission.objects.filter(user=self).values_list('document__id', flat=True)),
                    list(documents.models.Document.objects.filter(project__id__in=projects.models.ProjectPermission.objects.filter(user=self).values_list('project__id', flat=True)).values_list('id', flat=True)),
                    list(documents.models.Document.objects.filter(project__organization__id__in=organizations.models.OrganizationPermission.objects.filter(user=self).values_list('organization__id', flat=True)).values_list('id', flat=True))
                ])
            )

    def get_users(self):
        if self.is_superuser:
            return User.objects.all()
        else:
            organization_ids = self.get_organizations().values_list('id')
            return User.objects.filter(
                pk__in=set().union(*[
                    list(organizations.models.OrganizationPermission.objects.filter(organization__id__in=organization_ids).values_list('user__id', flat=True)),
                    list(projects.models.ProjectPermission.objects.filter(project__organization__id__in=organization_ids).values_list('user_id', flat=True)),
                    list(documents.models.DocumentPermission.objects.filter(document__project__organization__id__in=organization_ids).values_list('user_id', flat=True))
                ])
            )

    def send_invite(self, app, template, subject, object):
        template_txt = '{0}/{1}.txt'.format(app, template)
        if settings.USE_HTML_EMAIL:
            template_html = loader.get_template('{0}/{1}.html'.format(app, template))
        context = {
            'object': object,
            'user': self,
            'uid': urlsafe_base64_encode(force_bytes(self.pk)).decode(),
            'token': default_token_generator.make_token(self),
            'application_url': settings.APPLICATION_URL,
            'help_email': settings.HELP_EMAIL,
        }
        send_mail(
            subject,
            render_to_string(template_txt, context),
            settings.FROM_EMAIL,
            [self.email],
            fail_silently=False,
            #html_message=render(None, template_html, context) if settings.USE_HTML_EMAIL else None
        )

    def __str__(self):  # pragma: no cover
        return "{0} {1}".format(self.first_name, self.last_name)
