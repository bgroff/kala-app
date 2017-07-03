from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class CompaniesView(LoginRequiredMixin, TemplateView):
    template_name = 'companies/companies.html'

    def get_context_data(self, **kwargs):
        return {
            'companies': self.request.user.get_companies(has_projects=False),
        }
