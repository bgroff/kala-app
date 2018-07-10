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
            return organizations.models.Organization.objects.all()
        return organizations.models.Organization.objects.filter(
            uuid__in=Permissions.objects.filter(user=self, permission__codename='add_organization').values_list(
                'object_uuid', flat=True))

    def get_organizations(self):
        if self.is_superuser:
            return organizations.models.Organization.objects.active()
        project_uuids = Permissions.objects.filter(
            user=self,
            permission__codename__in=[
                'change_project',
                'add_project',
                'delete_project'
            ]
        ).values_list('object_uuid', flat=True)
        project_org_uuids = projects.models.Project.objects.filter(
            uuid__in=project_uuids
        ).values_list('organization__uuid', flat=True)
        org_uuids = Permissions.objects.filter(
            user=self,
            permission__codename__in=[
                'change_organization',
                'add_organization',
                'delete_organization'
            ]
        ).values_list('object_uuid', flat=True)
        document_project_uuids = Permissions.objects.filter(permission__codename__in=[
            'change_document',
            'add_document',
            'delete_document'
        ], user=self).values_list('object_uuid', flat=True)
        document_projects = documents.models.Document.objects.filter(
            uuid__in=document_project_uuids
        ).values_list('project__organization__uuid', flat=True)
        return organizations.models.Organization.objects.filter(
            uuid__in=list(project_org_uuids) + list(org_uuids) + list(document_projects)
        )

    def get_projects(self):
        if self.is_superuser:
            return projects.models.Project.objects.active()
        else:
            return projects.models.Project.objects.active().filter(
                organization__id__in=self.get_organizations().values_list('pk', flat=True)
            )

    def get_documents(self):
        if self.is_superuser:
            return documents.models.Document.objects.all()
        else:
            projects = self.get_organizations().values_list('project__uuid', flat=True)
            document_uuids = documents.models.Document.objects.filter(
                project__uuid__in=projects
            ).values_list('uuid', flat=True)

            perm_uuids = Permissions.objects.filter(
                user=self,
                object_uuid__in=document_uuids
            ).values_list('object_uuid', flat=True)

            return documents.models.Document.objects.filter(
                uuid__in=list(perm_uuids) + list(document_uuids)
            ).prefetch_related(
                'documentversion_set',
                'documentversion_set__user',
            ).select_related('project')

    def get_users(self):
        if self.is_superuser:
            return User.objects.all()
        else:
            organization_uuids = self.get_organizations().values_list('uuid')

            return User.objects.filter(pk__in=Permissions.perms_for_objects([
                'change_organization',
                'add_organization',
                'delete_organization'
            ], organization_uuids).distinct('user').values_list('user__pk', flat=True))

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

    def add_perm(self, perm, uuid):
        Permissions.add_perm(perm=perm, user=self, uuid=uuid)

    def has_perm(self, perm, uuid):
        return Permissions.has_perm(perm=perm, user=self, uuid=uuid)

    def add_read(self, user):
        perm = Permission.objects.get(codename='change_user')
        Permissions.add_perm(perm=perm, user=user, uuid=self.uuid)

    def has_read(self, user):
        perm = Permission.objects.get(codename='change_user')
        return Permissions.has_perm(perm=perm, user=user, uuid=self.uuid)

    def add_delete(self, user):
        perm = Permission.objects.get(codename='delete_user')
        Permissions.add_perm(perm=perm, user=user, uuid=self.uuid)

    def has_delete(self, user):
        perm = Permission.objects.get(codename='delete_user')
        return Permissions.has_perm(perm=perm, user=user, uuid=self.uuid)

    def add_create(self, user):
        perm = Permission.objects.get(codename='add_user')
        Permissions.add_perm(perm=perm, user=user, uuid=self.uuid)

    def has_create(self, user):
        perm = Permission.objects.get(codename='add_user')
        return Permissions.has_perm(perm=perm, user=user, uuid=self.uuid)

    def __str__(self):  # pragma: no cover
        return "{0} {1}".format(self.first_name, self.last_name)


class Permissions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.DO_NOTHING)
    object_uuid = models.UUIDField()

    @classmethod
    def has_perm(cls, perm, user, uuid):
        if user.is_superuser:
            return True
        try:
            cls.objects.get(user=user, permission=perm, object_uuid=uuid)
            return True
        except Permissions.DoesNotExist:
            return False
        return False

    @classmethod
    def has_perms(cls, perms, user, uuid):
        if user.is_superuser:
            return True
        return cls.objects.filter(user=user, permission__codename__in=perms, object_uuid=uuid).exists()

    @classmethod
    def add_perm(cls, perm, user, uuid):
        cls.objects.create(user=user, permission=perm, object_uuid=uuid)

    @classmethod
    def perms_for_objects(cls, perms, uuids):
        return cls.objects.filter(permission__codename__in=perms, object_uuid__in=uuids)
