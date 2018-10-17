from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView

from projects.forms import DetailsForm
from projects.models import Project


class DetailsView(TemplateView):
    template_name = 'projects/settings/details.html'

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

        self.form = DetailsForm(request.POST or None, instance=self.project)
        return super(DetailsView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save(commit=False)
            self.form.save_m2m()
            self.form.save()
            messages.success(request, _('The project has been updated.'))
            return redirect(reverse('projects:details', args=[self.project.pk]))
        return self.render_to_response(self.get_context_data())
