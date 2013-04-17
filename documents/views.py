from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View
from .forms import DocumentForm
from .models import Documents, DocumentVersion
from kala.views import LoginRequiredMixin
from people.models import People


class BaseDocumentView(LoginRequiredMixin, View):
    def check_permission(self):
        if not self.project.clients.filter(pk=self.request.user.pk).exists() and not self.request.user.is_admin:
            return False
        return True


class DocumentView(TemplateView, BaseDocumentView):
    template_name = 'document.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'document': self.document,
            'project': self.project,
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.document = get_object_or_404(Documents.active, pk=pk)
        self.person = get_object_or_404(People.active, pk=request.user.pk)
        self.project = self.document.project
        self.form = DocumentForm(request.POST or None, request.FILES or None, project=self.project,
                                 document=self.document, person=self.person)

        if not self.check_permission():
            messages.error(request, 'You do not have permission to download this file.')
            return redirect(reverse('home'))
        return super(DocumentView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save()
            messages.success(request, 'A new version of this document has been uploaded')
            return redirect(reverse('document', args=[self.document.pk]))
        return self.render_to_response(self.get_context_data())


class DownloadDocument(BaseDocumentView):
    """
    """

    def dispatch(self, request, pk, *args, **kwargs):
        self.document = get_object_or_404(DocumentVersion, pk=pk)
        self.project = self.document.document.project
        if not self.check_permission():
            messages.error(request, 'You do not have permission to download this file.')
            return redirect(reverse('home'))
        return super(DownloadDocument, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.document.build_http_response()
