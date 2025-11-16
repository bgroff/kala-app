from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import TemplateView

from documents.models import DocumentVersion
from projects.forms import CategoryForm, SortForm
from projects.models import Project
from projects.tasks.export_project import ExportProjectTask


class ProjectView(TemplateView):
    template_name = 'projects/project.html'

    def get_context_data(self, **kwargs):
        version_ids = []
        for document in self.documents:
            for version in document.documentversion_set.all():
                version_ids.append(str(version.uuid))
        versions = DocumentVersion.objects.filter(uuid__in=version_ids).order_by('user_id')

        sort_order = self.request.GET.get('sort', None)
        if sort_order:
            if sort_order == 'Alphabetically':
                self.documents = self.documents.order_by('name')
            else:
                self.documents = self.documents.order_by('-date')

        category = self.request.GET.get('category', None)
        if category:
            self.documents = self.documents.filter(category__name=category)

        # Filter by tag if specified
        tag = self.request.GET.get('tag', None)
        if tag:
            self.documents = self.documents.filter(tags__name=tag)

        # Filter by file extension if specified
        extension = self.request.GET.get('ext', None)
        if extension:
            self.documents = self.documents.filter(mime__icontains=extension)

        per_page = self.request.GET.get('per_page', 20)
        page = self.request.GET.get('page', 1)
        paginator = Paginator(self.documents, per_page)
        try:
            documents = paginator.page(page).object_list
        except InvalidPage:
            documents = paginator.page(1)

        # Get all unique tags used in the project's documents
        from taggit.models import Tag
        all_project_documents = self.project.get_documents(self.request.user)
        tag_ids = all_project_documents.values_list('tags', flat=True).distinct()
        project_tags = Tag.objects.filter(id__in=tag_ids).order_by('name')

        return {
            'categories_form': self.categories_form,
            'documents': documents,
            'page_range': paginator.page_range,
            'current_page': page,
            'project': self.project,
            'organization': self.project.organization,
            'sort_form': self.sort_form,
            'version_count': versions.count(),
            'user_count': versions.distinct('user').count(),
            'project_tags': project_tags
        }

    @method_decorator(login_required)
    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active().prefetch_related('category_set'), pk=pk)
        if not self.project.can_create(user=self.request.user):
            raise PermissionDenied(
                _('You do not have permission to view this project.')
            )
        self.categories_form = CategoryForm(request.GET or None, project=self.project)
        self.sort_form = SortForm(request.GET or None)
        documents = self.project.get_documents(request.user).prefetch_related(
            'documentversion_set',
            'documentversion_set__user'
        )
        if 'search' in request.GET and request.GET['search'] != '':
            search_term = request.GET.get('search', '')
            # Use Q objects with icontains for partial, case-insensitive matching
            # This allows finding "CourseDeliveryStatus" when searching for "Delivery"
            self.documents = documents.filter(
                id__in=DocumentVersion.objects.filter(
                    Q(name__icontains=search_term) |
                    Q(description__icontains=search_term) |
                    Q(user__first_name__icontains=search_term) |
                    Q(user__last_name__icontains=search_term) |
                    Q(user__username__icontains=search_term)
                ).values_list('document_id', flat=True)
            ).filter(project=self.project).prefetch_related('documentversion_set', 'documentversion_set__user')
            self.sort_order = request.GET.get('search')
        else:
            self.documents = documents

        return super(ProjectView, self).dispatch(request, *args, **kwargs)


class ExportProjectView(View):

    @method_decorator(login_required)
    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=pk)
        if not self.project.can_create(user=self.request.user):
            raise PermissionDenied(
                _('You do not have permission to view this project.')
            )
        return super(ExportProjectView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        task = ExportProjectTask()
        task.apply_async([self.project.pk, request.user.pk], queue=settings.EXPORT_QUEUE)
        messages.success(request, _('Your project has been scheduled for export. You will receive a download notification shortly.'))

        return redirect(
            reverse(
                'projects:project',
                args=[self.project.pk]
            )
        )
