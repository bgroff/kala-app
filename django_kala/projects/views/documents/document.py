from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from accounts.mixins import LoginRequiredMixin
from accounts.models import User
from documents.defs import get_mimes_for_category
from documents.forms import DocumentForm
from documents.models import Document
from projects.forms import CategoryForm, SortForm
from projects.models import Project


class DocumentView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/document.html'

    def get_context_data(self, **kwargs):
        return {
            'project': self.project,
            'document': self.document,
        }

    def dispatch(self, request, project_pk, document_pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=project_pk)
        self.document = get_object_or_404(
            Document.objects.active().prefetch_related(
                'documentversion_set',
                'documentversion_set__person'
            ),
            pk=document_pk)
        return super(DocumentView, self).dispatch(request, *args, **kwargs)
