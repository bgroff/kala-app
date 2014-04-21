from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from .models import Project
from .forms import CategoryForm, ProjectForm, SortForm, permission_forms, CompanyForm, DeleteProjectsForm
from accounts.mixins import LoginRequiredMixin, AdminRequiredMixin
from accounts.models import Person
from documents.defs import get_mimes_for_category
from documents.forms import DocumentForm
from documents.models import Document


class ProjectsView(LoginRequiredMixin, TemplateView):
    template_name = 'projects.html'

    def get_context_data(self, **kwargs):
        context = {
            'companies': self.request.user.get_companies(),
            'form': self.form,
            }
        if self.request.user.is_admin:
            context['deleted_form'] = self.deleted_form

        return context

    def dispatch(self, request, *args, **kwargs):
        self.form = ProjectForm(request.POST or None, company=request.user.company,
                                is_admin=self.request.user.is_admin)
        if request.user.is_admin:
            self.deleted_form = DeleteProjectsForm(request.POST or None)

        return super(ProjectsView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'You do not have permission to create a new project')
            return redirect(reverse('projects'))

        if 'create' in request.POST and self.form.is_valid():
            project = self.form.save()
            # Add everyone in the organization to the project.
            #[project.clients.add(person) for person in project.company.get_people_list()]
            messages.success(request, 'The project has been created')
            return redirect(reverse('project', args=[project.pk]))

        if 'undelete' in request.POST and self.deleted_form.is_valid():
            project = self.deleted_form.save()
            messages.success(request, 'The project %s has been un-deleted' % project.name)
            return redirect(reverse('projects'))

        return self.render_to_response(self.get_context_data())


class ProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'project.html'

    def get_context_data(self, **kwargs):
        documents = Document.objects.active().filter(project=self.project)
        if hasattr(self, 'sort_order'):
            if self.sort_order == 'AZ':
                documents = documents.order_by('name')
        if hasattr(self, 'category'):
            mimes = get_mimes_for_category(self.category)
            documents = documents.filter(mime__in=mimes)
        return {
            'categories_form': self.categories_form,
            'company_form': self.company_form,
            'documents': documents,
            'form': self.form,
            'project': self.project,
            'sort_form': self.sort_form,
            }

    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=pk)
        person = Person.objects.get(pk=self.request.user.pk)
        self.form = DocumentForm(request.POST or None, request.FILES or None, person=person,
                                 project=self.project)
        self.categories_form = CategoryForm(request.GET or None, project=self.project)
        self.company_form = CompanyForm(request.POST or None, project=self.project)
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

        if 'move' in request.POST and request.user.is_admin and self.company_form.is_valid():
            self.company_form.save()
            return redirect(reverse('project', args=[self.project.pk]))

        if 'upload' in request.POST and self.form.is_valid():
            self.form.save()
            messages.success(request, 'The document has been created')
            return redirect(reverse('project', args=[self.project.pk]))
        return self.render_to_response(self.get_context_data())


class ProjectPermissions(AdminRequiredMixin, TemplateView):
    template_name = 'permissions.html'

    def get_context_data(self, **kwargs):
        return {
            'forms': self.forms,
            'project': self.project,
            }

    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=pk)
        self.forms = permission_forms(request, self.project)
        return super(ProjectPermissions, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        all_valid = True
        for form in self.forms:
            if form.is_valid():
                form.save()
            else:
                all_valid = False
        if all_valid:
            messages.success(request, 'The permissions have been updated.')
            return redirect(reverse('permissions', args=[self.project.pk]))
        return self.render_to_response(self.get_context_data())
