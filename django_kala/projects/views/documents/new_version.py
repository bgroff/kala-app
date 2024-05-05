from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView

from documents.models import Document
from projects.forms.documents.new_version import NewDocumentVersionForm
from projects.models import Project


class NewDocumentVersionView(TemplateView):
    template_name = 'documents/new_version.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'document': self.document,
            'project': self.project,
            'organization': self.project.organization
        }

    @method_decorator(login_required)
    def dispatch(self, request, project_pk, document_pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=project_pk)
        self.document = get_object_or_404(Document.objects.active(), pk=document_pk)
        if not self.document.can_create(self.request.user):
            raise PermissionDenied(_('You do not have permission to create a new version for this document.'))

        self.form = NewDocumentVersionForm(
            request.POST or None,
            request.FILES or None,
            document=self.document,
            project=self.project,
            user=request.user
        )
        return super(NewDocumentVersionView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            version = self.form.save(commit=False)
            version.name = request.FILES['file'].name
            version.mime = request.FILES['file'].content_type
            version.save()
            messages.success(request, _('The version has been saved.'))
            return redirect(reverse('projects:document', args=[self.project.pk, self.document.pk]))
        return self.render_to_response(self.get_context_data())
