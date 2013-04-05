from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from documents.forms import PersonForm
from documents.models import Document, Company, Project


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        return {
            'companies': Company.objects.all(),
            'documents': Document.objects.all()[:10]
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


class Projects(TemplateView):
    template_name = 'projects.html'

    def get_context_data(self, **kwargs):
        return {
            'my_company': self.request.user.company,
            'companies': Company.objects.all(),
        }


class ProjectView(TemplateView):
    template_name = 'project.html'

    def get_context_data(self, **kwargs):
        return {
            'project': self.project,
            'documents': Document.objects.filter(project=self.project)
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=pk)
        return super(ProjectView, self).dispatch(request, *args, **kwargs)
