from django.db import models
from django.db.models.query import QuerySet


class ActiveMixin(object):
    def active(self):
        return self.filter(is_active=True)

    def deleted(self):
        return self.filter(is_active=False)


class ActiveQuerySet(QuerySet, ActiveMixin):
    pass


class ActiveManager(models.Manager, ActiveMixin):
    def get_query_set(self):
        return ActiveQuerySet(self.model, using=self._db)
