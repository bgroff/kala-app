from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from accounts.mixins import LoginRequiredMixin
from projects.forms import ProjectForm, DeleteProjectsForm


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
        self.form = ProjectForm(request.POST or None, company=request.user.companies,
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
            # [project.clients.add(person) for person in project.company.get_people_list()]
            messages.success(request, 'The project has been created')
            return redirect(reverse('project', args=[project.pk]))

        if 'undelete' in request.POST and self.deleted_form.is_valid():
            project = self.deleted_form.save()
            messages.success(request, 'The project %s has been un-deleted' % project.name)
            return redirect(reverse('projects'))

        return self.render_to_response(self.get_context_data())

