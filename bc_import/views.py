from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, HttpResponse, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from ndptc.accounts.mixins import LoginRequiredMixin
from .models import BCDocumentVersion
from .tasks import import_groups, download_document
from .forms import BasecampAuthorizationForm


class BasecampAuthorize(LoginRequiredMixin, TemplateView):
    template_name = 'basecamp_authorization.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
        }

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.form = BasecampAuthorizationForm(request.POST or None)
        return super(BasecampAuthorize, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            bc_auth =  signing.dumps({
                'bc_name': self.form.cleaned_data['name'],
                'username': self.form.cleaned_data['username'],
                'password': self.form.cleaned_data['password'],
            })
            request.session['bc_auth'] = bc_auth
            messages.success(request, 'Your account has been authorized')
            return redirect(reverse('basecamp_import'))
        return self.render_to_response(self.get_context_data())


class BasecampUnauthorize(View):
    def get(self, request, *args, **kwargs):
        if 'bc_auth' in request.session:
            del request.session['bc_auth']
        messages.success(request, 'Your account has been unauthorized')
        return redirect(reverse('basecamp_authorize'))


class BasecampImport(TemplateView):
    template_name = 'basecamp_import.html'

    def get_context_data(self, **kwargs):
        return {
            'name': self.bc_auth['bc_name'],
        }

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if 'bc_auth' not in request.session:
            messages.error(request, 'You have not authorized any basecamp projects')
            return redirect(reverse('basecamp_authorize'))
        self.bc_auth = signing.loads(request.session.get('bc_auth'))
        return super(BasecampImport, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'update-information' in request.POST:
            import_groups.delay(self.bc_auth['bc_name'], self.bc_auth['username'], self.bc_auth['password'])

        if 'update-documents' in request.POST:
            documents = BCDocumentVersion.objects.filter(file='')
            for document in documents:
                download_document.delay(document, self.bc_auth['username'], self.bc_auth['password'])

        return self.render_to_response(self.get_context_data())


class BasecampDownloadDocument(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if 'bc_auth' not in request.session:
            messages.error(request, 'You have not authorized any basecamp projects')
            return redirect(reverse('basecamp_authorize'))
        self.bc_auth = signing.loads(request.session.get('bc_auth'))
        return super(BasecampDownloadDocument, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        document = get_object_or_404(BCDocumentVersion, pk=pk)
        task = download_document.delay(document, self.bc_auth['username'], self.bc_auth['password'])
        return HttpResponse("{'worked': 'true'}", content_type='application/json')
