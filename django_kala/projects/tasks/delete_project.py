from django.conf import settings
from django.contrib.auth import get_user_model

from projects.models import Project
from projects.tasks.delete_document import DeleteDocumentTask

User = get_user_model()


class DeleteProjectTask():

    def run(self, *args, **kwargs):
        self.project = Project.objects.get(pk=args[0])
        user = User.objects.get(pk=args[1])
        if not self.project.can_manage(user):
            # TODO: Log this
            return
        for document in self.project.document_set.all():
            manager = settings.PLATFORM_MANAGER()
            manager.delete_document(document)

    def on_success(self, retval, task_id, args, kwargs):
        self.project.delete()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # TODO: Log this
        return
