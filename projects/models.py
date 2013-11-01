import datetime
from accounts.models import Person
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from documents.models import Document
from kala.managers import ActiveManager


@python_2_unicode_compatible
class Project(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey('companies.Company')
    clients = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    removed = models.DateField(null=True)
    changed = models.DateTimeField(auto_now=True, auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = ActiveManager()

    class Meta:
        ordering = ('name',)
        db_table = 'kala_projects'

    def set_active(self, active):
        assert type(active) is bool, 'The active parameter must be of type bool.'
        self.is_active = active
        for document in Document.objects.filter(project=self):
            document.set_active(active)
        if not self.is_active:
            self.removed = datetime.date.today()
        self.save()

    def add_client(self, client):
        assert type(client) is Person, 'The client parameter must be of type People.' # Solient Green

        # Check if the client is in the clients list, add if not.
        try:
            self.clients.get(client)
        except Person.DoesNotExist:
            self.clients.add(client)

    def remove_client(self, client):
        assert type(client) is Person, 'The client parameter must be of type People.'
        self.clients.remove(client)

    def __str__(self):
        return self.name
