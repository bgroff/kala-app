from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from documents.models import Document
from projects.models import Project


class DocumentView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/document.html'

    def get_context_data(self, **kwargs):
        return {
            'project': self.project,
            'document': self.document,
            'can_change': self.document.has_change(self.request.user),
            'can_create': self.has_change or self.has_create,
            'can_invite': self.project.organization.has_change(self.request.user) or self.project.organization.has_create(self.request.user)
        }

    def dispatch(self, request, project_pk, document_pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=project_pk)
        self.document = get_object_or_404(
            Document.objects.active().prefetch_related(
                'documentversion_set',
                'documentversion_set__user'
            ),
            pk=document_pk)
        self.has_create = self.document.has_create(request.user)
        self.has_change = self.document.has_change(request.user)
        if not self.has_create and not self.has_change and not self.document.has_delete(request.user):
            raise PermissionDenied('You do not have permissions to view this document.')
        return super(DocumentView, self).dispatch(request, *args, **kwargs)
