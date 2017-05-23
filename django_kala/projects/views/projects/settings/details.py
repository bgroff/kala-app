from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from accounts.mixins import AdminRequiredMixin
from projects.models import Project
from projects.forms import DetailsForm


class DetailsView(AdminRequiredMixin, TemplateView):
    template_name = 'projects/settings/details.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'project': self.project,
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=pk)
        self.form = DetailsForm(request.POST or None, instance=self.project)
        return super(DetailsView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save(commit=False)
            self.form.save_m2m()
            self.form.save()
            return redirect(reverse('projects:details', args=[self.project.pk]))
        return self.render_to_response(self.get_context_data())
