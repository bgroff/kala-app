from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from accounts.mixins import LoginRequiredMixin
from projects.forms import NewProjectForm


class NewProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'new_project.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
        }

    def dispatch(self, request, *args, **kwargs):
        self.form = NewProjectForm(request.POST or None, request.FILES or None, user=request.user)
        return super(NewProjectView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            project = self.form.save()
            return redirect(reverse('projects:project', args=[project.pk]))
        return self.render_to_response(self.get_context_data())
