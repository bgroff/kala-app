import datetime
from django.conf import settings
from django.db import models
from documents.models import Documents
from kala.managers import ActiveManager, DeletedManager
from people.models import People


class Projects(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey('companies.Companies')
    clients = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    removed = models.DateField(null=True)
    changed = models.DateTimeField(auto_now=True, auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveManager()
    deleted = DeletedManager()

    def set_active(self, active):
        assert type(active) is bool, 'The active parameter must be of type bool.'
        self.is_active = active
        for document in Documents.objects.filter(project=self):
            document.set_active(active)
        if not self.is_active:
            self.removed = datetime.date.today()
        self.save()

    def add_client(self, client):
        assert type(client) is People, 'The client parameter must be of type People.' # Solient Green

        # Check if the client is in the clients list, add if not.
        try:
            self.clients.get(client)
        except People.DoesNotExist:
            self.clients.add(client)

    def remove_client(self, client):
        assert type(client) is People, 'The client parameter must be of type People.'
        self.clients.remove(client)

    def __str__(self):
        return self.name
