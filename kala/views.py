from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from documents.models import Documents, DocumentVersion
from projects.models import Projects


class AdminRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'You must be an administrator to access this part of the application.')
            return redirect(reverse('home'))
        return super(AdminRequiredMixin, self).dispatch(request, *args, **kwargs)


class AdminEditRequiredMixin(object):

    def post(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'You must be an administrator to access this part of the application.')
            return redirect(reverse('home'))
        return super(AdminEditRequiredMixin, self).post(request, *args, **kwargs)


class LoginRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        return login_required()(super(LoginRequiredMixin, self).dispatch)(request, *args, **kwargs)


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        return {
            'companies': self.request.user.get_companies_list(),
            'documents': Documents.active.filter(pk__in=DocumentVersion.objects.filter(person=self.request.user.pk).values('document__pk'))[:10],
        }


class AttributionView(TemplateView):
    template_name = 'attribution.html'


class LicenseView(TemplateView):
    template_name = 'license.html'