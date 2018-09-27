from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView

from documents.models import Document


class ArchiveView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/settings/archive.html'

    def get_context_data(self, **kwargs):
        return {
            'document': self.document,
            'project': self.project,
            'organization': self.project.organization,
            'can_create': self.project.can_create(self.request.user),
            'can_invite': self.project.can_invite(self.request.user)
        }

    def dispatch(self, request, project_pk, document_pk, *args, **kwargs):
        self.document = get_object_or_404(
            Document.objects.active().select_related(
                'project',
                'project__organization'
            ),
            pk=document_pk
        )
        if not self.document.can_manage(request.user):
            raise PermissionDenied(_('You do not have permission to archive this document'))
        self.project = self.document.project

        return super(ArchiveView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.document.set_active(False)
        return redirect(
            reverse(
                'projects:document_archive',
                args=[
                    self.document.project.pk,
                    self.document.pk
                ]
            )
        )
