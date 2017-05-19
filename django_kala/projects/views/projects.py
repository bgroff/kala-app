from django.views.generic import TemplateView

from accounts.mixins import LoginRequiredMixin


class ProjectsView(LoginRequiredMixin, TemplateView):
    template_name = 'projects.html'

    def get_context_data(self, **kwargs):
        return {
            'companies': self.request.user.get_companies(),
        }
