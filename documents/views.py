from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, View, DeleteView
from django.views.generic.edit import DeletionMixin
from documents.forms import PersonForm, DocumentForm, ProjectForm, CompanyForm, CreateCompanyForm, CreatePersonForm, \
    permission_forms
from documents.models import Document, Company, Project, Person, DocumentVersion


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        return {
            'companies': self.request.user.get_companies_list(),
            'documents': Document.active.all()[:10]
        }


class CreateAccount(TemplateView):
    template_name = 'create_account.html'

    def get_context_data(self, **kwargs):
        return {'form': self.form}

    def dispatch(self, request, *args, **kwargs):
        self.form = PersonForm(self.request.POST or None)
        return super(CreateAccount, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        if self.form.is_valid():
            self.form.save()
            return redirect(reverse('home'))
        return self.render_to_response(self.get_context_data())


class EditProfile(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'person': self.person,
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.person = get_object_or_404(Person, pk=pk)
        if self.person != request.user and not request.user.is_admin:
            messages.error(request, 'You do not have permission to edit this persons account.')
            return redirect(reverse('home'))
        self.form = PersonForm(request.POST or None, instance=self.person)
        return super(EditProfile, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save()
            return redirect(reverse('edit_profile', args=[self.person.pk]))
        return self.render_to_response(self.get_context_data())


class Projects(TemplateView):
    template_name = 'projects.html'

    def get_context_data(self, **kwargs):
        return {
            'companies': self.request.user.get_companies_list(),
            'form': self.form,
        }

    def dispatch(self, request, *args, **kwargs):
        self.form = ProjectForm(request.POST or None, company=request.user.company,
                                is_admin=self.request.user.is_admin)
        return super(Projects, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'You do not have permission to create a new project.')
            return redirect(reverse('projects'))

        if self.form.is_valid():
            project = self.form.save()
            return redirect(reverse('project', args=[project.pk]))
        return self.render_to_response(self.get_context_data())


class ProjectView(TemplateView):
    template_name = 'project.html'

    def get_context_data(self, **kwargs):
        return {
            'documents': Document.active.filter(project=self.project),
            'form': self.form,
            'project': self.project,
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=pk)
        person = Person.objects.get(pk=self.request.user.pk)
        self.form = DocumentForm(request.POST or None, request.FILES or None, person=person,
                                 project=self.project)
        return super(ProjectView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save()
            return redirect(reverse('project', args=[self.project.pk]))
        return self.render_to_response(self.get_context_data())


class Documents(TemplateView):
    template_name = 'documents.html'


class DocumentView(TemplateView):
    template_name = 'document.html'


class DownloadDocument(View):
    """
    """
    def get(self, request, pk):
        document = get_object_or_404(DocumentVersion, pk=pk)
        return document.build_http_response()


class People(TemplateView):
    template_name = 'people.html'

    def get_context_data(self, **kwargs):
        return {
            'companies': self.companies,
            'company_form': self.company_form,
            'person_form': self.person_form,
        }

    def dispatch(self, request, *args, **kwargs):
        self.companies = Company.active.all()

        self.company_form = CreateCompanyForm(request.POST if 'create_company' in request.POST else None)
        self.person_form = CreatePersonForm(request.POST if 'create_person' in request.POST else None)
        return super(People, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'You do not have permission to create a new company.')
            return redirect(reverse('people'))

        if 'create_company' in request.POST and self.company_form.is_valid():
            company = self.company_form.save()
            return redirect(reverse('people', args=[company.pk]))
        if 'create_person' in request.POST and self.person_form.is_valid():
            self.person_form.save()
            return redirect(reverse('people'))
        return self.render_to_response(self.get_context_data())


class CompanyView(TemplateView):
    template_name = 'company.html'
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']

    def get_context_data(self, **kwargs):
        return {
            'company': self.company,
            'form': self.form,
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.company = get_object_or_404(Company, pk=pk)
        self.form = CompanyForm(request.POST or None, instance=self.company)
        return super(CompanyView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'You do not have permission to edit a new company.')
            return redirect(reverse('company', args=[self.company.pk]))

        if 'delete' in request.POST:
            self.company.set_active(False)
            return redirect(reverse('people'))

        if self.form.is_valid():
            company = self.form.save()
            return redirect(reverse('company', args=[self.company.pk]))

        return self.render_to_response(self.get_context_data())


class ProjectPermissions(TemplateView):
    template_name = 'permissions.html'

    def get_context_data(self, **kwargs):
        return {
            'forms': self.forms,
            'project': self.project,
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=pk)
        self.forms = permission_forms(request, self.project)
        return super(ProjectPermissions, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        for form in self.forms:
            if form.is_valid():
                form.save()
        return self.render_to_response(self.get_context_data())
