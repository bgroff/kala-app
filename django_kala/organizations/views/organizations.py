from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class OrganizationsView(LoginRequiredMixin, TemplateView):
    template_name = 'organizations/organizations.html'

    def get_context_data(self, **kwargs):
        return {
            'organizations': self.request.user.get_organizations(),
            'can_create': self.request.user.is_superuser,
        }
