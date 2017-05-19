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


class ProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'project.html'

    def get_context_data(self, **kwargs):
        documents = Document.objects.active().filter(project=self.project).select_related().prefetch_related(
            'documentversion_set',
            'documentversion_set__person'
        )

        if hasattr(self, 'sort_order'):
            if self.sort_order == 'AZ':
                documents = documents.order_by('name')
        if hasattr(self, 'category'):
            mimes = get_mimes_for_category(self.category)
            documents = documents.filter(mime__in=mimes)
        per_page = self.request.GET.get('per_page', 20)
        page = self.request.GET.get('page', 1)
        paginator = Paginator(documents, per_page)
        try:
            documents = paginator.page(page).object_list
        except InvalidPage:
            documents = paginator.page(1)
        return {
            'categories_form': self.categories_form,
            'documents': documents,
            'page_range': paginator.page_range,
            'current_page': page,
            'form': self.form,
            'project': self.project,
            'sort_form': self.sort_form,
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=pk)
        person = User.objects.get(pk=self.request.user.pk)
        self.form = DocumentForm(request.POST or None, request.FILES or None, person=person,
                                 project=self.project)
        self.categories_form = CategoryForm(request.GET or None, project=self.project)
        self.sort_form = SortForm(request.GET or None)
        if 'search' in request.GET:
            self.sort_order = request.GET.get('search')
        if 'category' in request.GET and request.GET.get('category'):
            self.category = request.GET.get('category')
        return super(ProjectView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST and request.user.is_admin:
            self.project.set_active(False)
            messages.success(request, 'The project has been deleted')
            return redirect(reverse('projects'))

        if 'upload' in request.POST and self.form.is_valid():
            self.form.save()
            messages.success(request, 'The document has been created')
            return redirect(reverse('project', args=[self.project.pk]))
        return self.render_to_response(self.get_context_data())

