from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView

from documents.models import Document
from projects.forms.documents.settings.transfer_ownership import TransferOwnershipForm
from projects.models import Project


class TransferOwnershipView(TemplateView):
    template_name = 'documents/settings/transfer_ownership.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'project': self.project,
            'organization': self.project.organization,
            'document': self.document
        }

    @method_decorator(login_required)
    def dispatch(self, request, project_pk, document_pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=project_pk)
        self.document = get_object_or_404(Document.objects.active(), pk=document_pk)
        if not self.document.can_manage(request.user):
            raise PermissionDenied(_('You do not have permission to edit this document'))

        self.form = TransferOwnershipForm(
            request.POST or None,
            document=self.document,
            projects=request.user.get_projects(['can_manage'])
        )
        return super(TransferOwnershipView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save()
            messages.success(request, _('The document has been transferred.'))
            return redirect(reverse('projects:document_transfer_ownership', args=[self.document.project.pk, self.document.pk]))
        return self.render_to_response(self.get_context_data())
