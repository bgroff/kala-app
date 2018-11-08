from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView

from documents.models import Document
from projects.tasks.delete_document import DeleteDocumentTask


class DeleteView(TemplateView):
    template_name = 'documents/settings/delete.html'

    def get_context_data(self, **kwargs):
        return {
            'document': self.document,
            'project': self.project,
            'organization': self.project.organization
        }

    @method_decorator(login_required)
    def dispatch(self, request, project_pk, document_pk, *args, **kwargs):
        self.document = get_object_or_404(
            Document.objects.active().select_related(
                'project',
                'project__organization'
            ),
            pk=document_pk
        )
        if not self.document.can_manage(request.user):
            raise PermissionDenied(_('You do not have permission to delete this document'))
        self.project = self.document.project

        return super(DeleteView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.document.set_active(False)
        DeleteDocumentTask().apply_async([self.document.pk, request.user.pk])
        messages.success(request, _('The document has been delete.'))
        return redirect(
            reverse(
                'projects:project',
                args=[
                    self.document.project.pk,
                ]
            )
        )
