from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView

from documents.models import Document
from projects.models import Project
from projects.forms.documents.settings.details import DetailsForm


class DocumentDetailsView(TemplateView):
    template_name = 'documents/settings/details.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'document': self.document,
            'project': self.project,
            'organization': self.project.organization
        }

    @method_decorator(login_required)
    def dispatch(self, request, project_pk, document_pk, *args, **kwargs):
        view = super(DocumentDetailsView, self)
        self.project = get_object_or_404(Project.objects.active(), pk=project_pk)
        self.document = get_object_or_404(Document.objects.active(), pk=document_pk)

        if not self.document.can_manage(request.user):
            raise PermissionDenied(_('You do not have permission to edit this project'))

        self.form = DetailsForm(request.POST or None, instance=self.document, project=self.project)
        return view.dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save(commit=False)
            self.form.save_m2m()
            self.form.save()
            messages.success(request, _('The document has been updated.'))
            return redirect(reverse('projects:document_details', args=[self.project.pk, self.document.pk]))
        return self.render_to_response(self.get_context_data())
