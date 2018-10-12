from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views import View
from django.views.generic import TemplateView

from documents.models import Document
from projects.models import Project
from projects.tasks.export_document import ExportDocumentTask


class DocumentView(TemplateView):
    template_name = 'documents/document.html'

    def get_context_data(self, **kwargs):
        return {
            'project': self.project,
            'organization': self.project.organization,
            'document': self.document
        }

    @method_decorator(login_required)
    def dispatch(self, request, project_pk, document_pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=project_pk)
        self.document = get_object_or_404(
            Document.objects.active().prefetch_related(
                'documentversion_set',
                'documentversion_set__user'
            ),
            pk=document_pk
        )
        if not self.document.can_create(request.user):
            raise PermissionDenied(_('You do not have permissions to view this document.'))
        return super(DocumentView, self).dispatch(request, *args, **kwargs)


class ExportDocumentView(View):

    @method_decorator(login_required)
    def dispatch(self, request, project_pk, document_pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=project_pk)
        self.document = get_object_or_404(Document.objects.active(), pk=document_pk)

        if not self.document.can_create(request.user):
            raise PermissionDenied(_('You do not have permissions to view this document.'))
        return super(ExportDocumentView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        task = ExportDocumentTask()
        task.apply_async([self.document.pk, request.user.pk], queue=settings.EXPORT_QUEUE)

        return redirect(
            reverse(
                'projects:document',
                args=[self.project.pk, self.document.pk]
            )
        )
