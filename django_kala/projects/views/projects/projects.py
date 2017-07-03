from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ProjectsView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/projects.html'

    def get_context_data(self, **kwargs):
        return {
            'companies': self.request.user.get_companies(),
        }
