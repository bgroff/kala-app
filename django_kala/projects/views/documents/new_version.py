from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from accounts.mixins import AdminRequiredMixin
from documents.models import Document
from projects.models import Project
from projects.forms.documents.new_version import NewDocumentVersionForm


class NewDocumentVersionView(AdminRequiredMixin, TemplateView):
    template_name = 'documents/new_version.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'document': self.document,
            'project': self.project
        }

    def dispatch(self, request, project_pk, document_pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=project_pk)
        self.document = get_object_or_404(Document.objects.active(), pk=document_pk)
        self.form = NewDocumentVersionForm(
            request.POST or None,
            request.FILES or None,
            document=self.document,
            project=self.project,
            person=request.user
        )
        return super(NewDocumentVersionView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            version = self.form.save(commit=False)
            version.name = request.FILES['file'].name
            version.mime = request.FILES['file'].content_type
            version.save()
            return redirect(reverse('projects:document', args=[self.project.pk, self.document.pk]))
        return self.render_to_response(self.get_context_data())
