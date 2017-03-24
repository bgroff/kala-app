from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from managers import ActiveManager

import datetime


class Project(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey('companies.Company')
    clients = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    removed = models.DateField(null=True)
    changed = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = ActiveManager()

    class Meta:
        ordering = ('name',)
        db_table = 'kala_projects'

    def set_active(self, active):
        self.is_active = active
        for document in self.document_set.all():
            document.set_active(active)
        if not self.is_active:
            self.removed = datetime.date.today()
        self.save()

    def add_client(self, client):
        # Check if the client is in the clients list, add if not.
        try:
            self.clients.get(client)
        except ObjectDoesNotExist:
            self.clients.add(client)

    def remove_client(self, client):
        self.clients.remove(client)

    def __str__(self):
        return self.name
