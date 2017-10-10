from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from auth.models import Permissions
from documents.defs import get_mimes_for_category
from documents.models import Document, DocumentVersion
from projects.forms import CategoryForm, SortForm
from projects.models import Project



class ProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/project.html'

    def get_context_data(self, **kwargs):
        version_ids = []
        for document in self.documents:
            for version in document.documentversion_set.all():
                version_ids.append(str(version.uuid))
        versions = DocumentVersion.objects.filter(uuid__in=version_ids).order_by('user_id')

        if hasattr(self, 'sort_order'):
            if self.sort_order == 'AZ':
                self.documents = self.documents.order_by('name')
        if hasattr(self, 'category'):
            mimes = get_mimes_for_category(self.category)
            self.documents = self.documents.filter(mime__in=mimes)
        per_page = self.request.GET.get('per_page', 20)
        page = self.request.GET.get('page', 1)
        paginator = Paginator(self.documents, per_page)
        try:
            documents = paginator.page(page).object_list
        except InvalidPage:
            documents = paginator.page(1)
        return {
            'categories_form': self.categories_form,
            'documents': documents,
            'page_range': paginator.page_range,
            'current_page': page,
            'project': self.project,
            'sort_form': self.sort_form,
            'version_count': versions.count(),
            'user_count': versions.distinct('user').count()
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=pk)
        if not Permissions.has_perms(
                [
                    'change_project',
                    'add_project',
                    'delete_project'
                ], request.user, self.project.uuid) and not Permissions.has_perms([
                    'change_organization',
                    'add_organization',
                    'delete_organization'
                ], request.user, self.project.organization.uuid) and not self.project.document_set.filter(
            uuid__in=Permissions.objects.filter(
                permission__codename__in=[
                    'change_document',
                    'add_document',
                    'delete_document'
                ], user=request.user).values_list('object_uuid', flat=True)).exists():
            raise PermissionDenied(
                'You do not have permission to view this project.'
            )
        self.categories_form = CategoryForm(request.GET or None, project=self.project)
        self.sort_form = SortForm(request.GET or None)
        documents = self.project.get_documents(request.user)
        if 'search' in request.GET and request.GET['search'] != '':
            self.documents = documents.filter(
                id__in=DocumentVersion.objects.annotate(
                    search=SearchVector('name', 'description')
                ).filter(
                    search=request.GET.get('search', '')
                ).values_list('document_id', flat=True)
            ).filter(project=self.project).prefetch_related('documentversion_set', 'documentversion_set__user')
            self.sort_order = request.GET.get('search')
        else:
            self.documents = documents

        return super(ProjectView, self).dispatch(request, *args, **kwargs)
