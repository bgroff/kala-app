from django.conf import settings
from django.contrib.auth import get_user_model

from organizations.models import Organization

User = get_user_model()


# TODO: let this work with Celery
class DeleteOrganizationTask():

    def run(self, *args, **kwargs):
        self.organization = Organization.objects.get(pk=args[0])
        user = User.objects.get(pk=args[1])
        if not self.organization.can_manage(user):
            # TODO: Log this
            return
        for project in self.organization.project_set.all():
            for document in project.document_set.all():
                manager = settings.PLATFORM_MANAGER()
                manager.delete_document(document)

    def on_success(self, retval, task_id, args, kwargs):
        self.organization.delete()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # TODO: Log this
        return
