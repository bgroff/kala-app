from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView

from projects.forms import TransferOwnershipForm
from projects.models import Project


class TransferOwnershipView(TemplateView):
    template_name = 'projects/settings/transfer_ownership.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'project': self.project,
            'organization': self.project.organization
        }

    @method_decorator(login_required)
    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=pk)
        if not self.project.can_manage(request.user):
            raise PermissionDenied(_('You do not have permission to edit this project'))

        self.form = TransferOwnershipForm(
            request.POST or None,
            project=self.project,
            organizations=request.user.get_organizations(['can_manage'])
        )
        return super(TransferOwnershipView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save()
            messages.success(request, _('The project has been transferred.'))
            return redirect(reverse('projects:transfer_ownership', args=[self.project.pk]))
        return self.render_to_response(self.get_context_data())
