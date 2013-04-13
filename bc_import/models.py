from django.db import models
from documents.models import DocumentVersion, Company, Person, Project


class BCCompany(Company):
    # remove when done
    bc_id = models.IntegerField()


class BCDocumentVersion(DocumentVersion):
    def __init__(self, *args, **kwargs):
        super(BCDocumentVersion, self).__init__(*args, **kwargs)
        self.file.field.null = True
        for field in self._meta.local_fields:
            if field.name == 'created':
                field.auto_add_now = False
            elif field.name == 'changed':
                field.auto_now_add = False

    bc_latest = models.BooleanField()
    bc_size = models.IntegerField()
    bc_collection = models.IntegerField()
    bc_id = models.IntegerField()
    bc_project = models.ForeignKey(Project)
    bc_category = models.IntegerField(null=True, blank=True)
    bc_url = models.URLField(max_length=400)


#should probably use AbstractBaseUser as the 30 char limit on users names is difficult.
class BCPerson(Person):
    bc_id = models.IntegerField(null=True, blank=True)


class BCProject(Project):
    bc_id = models.IntegerField()
