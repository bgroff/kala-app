from django.conf import settings
from django.contrib.auth import get_user_model

from documents.models import Document

User = get_user_model()


class DeleteDocumentTask():

    def run(self, *args, **kwargs):
        self.document = Document.objects.get(pk=args[0])
        user = User.objects.get(pk=args[1])
        if not self.document.can_manage(user):
            # TODO: Log this
            return
        manager = settings.PLATFORM_MANAGER()
        manager.delete_document(self.document)

    def on_success(self, retval, task_id, args, kwargs):
        self.document.delete()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # TODO: Log this
        return
