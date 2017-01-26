from django.contrib.auth import get_user
from django.views.generic import TemplateView
from accounts.mixins import LoginRequiredMixin
from documents.models import Document, DocumentVersion


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        return {
            'companies': self.request.user.get_companies(),
            'documents': Document.objects.active().filter(
                pk__in=DocumentVersion.objects.filter(person=get_user(self.request)).values('document__pk'))[:10],
        }


class UserDocumentationView(LoginRequiredMixin, TemplateView):
    template_name = 'user_documentation.html'


class LicenseView(TemplateView, LoginRequiredMixin):
    template_name = 'license.html'
