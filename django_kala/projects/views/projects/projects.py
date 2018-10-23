from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ProjectsView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/projects.html'

    def get_context_data(self, **kwargs):
        return {
            'can_create': True if self.request.user.get_organizations_with_create() else False,
            'organizations': self.request.user.get_organizations(),
        }
