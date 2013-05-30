from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from documents.models import Documents, DocumentVersion


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
    login_url = settings.LOGIN_URL
    redirect_field_name = REDIRECT_FIELD_NAME
    raise_exception = False

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            if self.raise_exception:
                raise PermissionDenied  # return a forbidden response
            else:
                return redirect_to_login(request.get_full_path(),
                    self.login_url, self.redirect_field_name)
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        return {
            'companies': self.request.user.get_companies_list(),
            'documents': Documents.active.filter(
                pk__in=DocumentVersion.objects.filter(person_id=self.request.user.pk).values('document__pk'))[:10],
        }


class UserDocumentationView(TemplateView):
    template_name = 'user_documentation.html'


class LicenseView(TemplateView):
    template_name = 'license.html'