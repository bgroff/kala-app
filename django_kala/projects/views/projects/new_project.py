from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from projects.forms import NewProjectForm


class NewProjectView(TemplateView):
    template_name = 'projects/new_project.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
        }

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.organizations = request.user.get_organizations_with_create()
        if not self.organizations:
            raise PermissionDenied(_('You do not have permissions to create projects.'))
        self.form = NewProjectForm(
            request.POST or None,
            request.FILES or None,
            user=request.user,
            organizations=self.organizations
        )
        return super(NewProjectView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            project = self.form.save()
            messages.success(request, _('The project has been saved.'))
            return redirect(reverse('projects:project', args=[project.pk]))
        return self.render_to_response(self.get_context_data())
