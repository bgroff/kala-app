from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views import View

from documents.models import Document, DocumentVersion
from projects.models import Project


class DocumentDownload(LoginRequiredMixin, View):
    """
    """

    def dispatch(self, request, project_pk, document_pk, version_uuid, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=project_pk)
        self.document = get_object_or_404(Document, pk=document_pk)
        self.version = get_object_or_404(DocumentVersion, uuid=version_uuid)

        if not self.document.can_create():
            raise PermissionDenied(_('You do not have permissions to view this document.'))

        return super(DocumentDownload, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.version.http_response()
