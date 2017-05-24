from django.views.generic import TemplateView

from ..mixins import LoginRequiredMixin


class UsersView(LoginRequiredMixin, TemplateView):
    template_name = 'users.html'

    def get_context_data(self, **kwargs):
        return {
            'users': self.request.user.get_users().prefetch_related('companies'),
            'companies': self.request.user.get_companies()
        }
