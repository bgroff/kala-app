from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator, InvalidPage
from django.views.generic import TemplateView

from documents.defs import get_mimes_for_category
from documents.models import Document, DocumentVersion
from projects.forms import SortForm


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        return {
            'organizations': self.request.user.get_organizations(),
            'documents': Document.objects.active().filter(
                pk__in=DocumentVersion.objects.filter(person=get_user(self.request)).values('document__pk'))[:10],
        }


class UserDocumentationView(LoginRequiredMixin, TemplateView):
    template_name = 'user_documentation.html'


class LicenseView(TemplateView, LoginRequiredMixin):
    template_name = 'license.html'


class SearchView(LoginRequiredMixin, TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        version_ids = []
        for document in self.documents:
            for version in document.documentversion_set.all():
                version_ids.append(str(version.uuid))
        versions = DocumentVersion.objects.filter(uuid__in=version_ids).order_by('person_id')

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
            'documents': documents,
            'page_range': paginator.page_range,
            'document_count': paginator.count,
            'current_page': page,
            'sort_form': self.sort_form,
            'version_count': versions.count(),
            'user_count': versions.distinct('person').count()
        }

    def dispatch(self, request, *args, **kwargs):
        self.sort_form = SortForm(request.GET or None)

        self.documents = Document.objects.filter(
            id__in=DocumentVersion.objects.annotate(
                search=SearchVector('name', 'description')
            ).filter(
                search=request.GET.get('search', '')
            ).values_list('document_id', flat=True)
        ).filter(
            project__in=request.user.get_projects()
        ).prefetch_related(
            'documentversion_set', 'documentversion_set__person', 'project'
        )
        self.sort_order = request.GET.get('search')

        return super(SearchView, self).dispatch(request, *args, **kwargs)
