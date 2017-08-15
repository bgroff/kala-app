from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from projects.forms import CategoryForm
from projects.models import Project, Category


class CategoriesView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/settings/categories.html'

    def get_context_data(self, **kwargs):
        return {
            'categories': self.project.category_set.all(),
            'project': self.project,
        }

    def dispatch(self, request, pk, category_pk=None, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=pk)
        if category_pk:
            self.category = get_object_or_404(Category, pk=category_pk)
        return super(CategoriesView, self).dispatch(request, *args, **kwargs)

    def delete(self, *args, **kwargs):
        # TODO: check permissions
        if self.category:
            self.category.delete()
            return HttpResponse(status=202)
        return self.render_to_response(self.get_context_data())


class NewCategoryView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/settings/new_category.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'project': self.project,
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=pk)
        self.form = CategoryForm(request.POST or None, project=self.project)
        return super(NewCategoryView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save()
            return redirect(reverse('projects:categories', args=[self.project.pk]))
        return self.render_to_response(self.get_context_data())


class EditCategoryView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/settings/edit_category.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'project': self.project,
        }

    def dispatch(self, request, project_pk, category_pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=project_pk)
        self.category = get_object_or_404(Category, pk=category_pk)
        self.form = CategoryForm(request.POST or None, instance=self.category, project=self.project)
        return super(EditCategoryView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save()
            return redirect(reverse('projects:edit_category', args=[self.project.pk, self.category.pk]))
        return self.render_to_response(self.get_context_data())
