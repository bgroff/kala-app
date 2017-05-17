
from .settings.details import DetailsForm
from .settings.manage_access import ManageAccessForm, manage_access_forms
from .settings.transfer_ownership import TransferOwnershipForm


from django import forms
from projects.models import Project
from companies.models import Company
from documents.defs import get_categories_for_mimes
from documents.models import Document


class CategoryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super(CategoryForm, self).__init__(*args, **kwargs)

        self.fields['category'] = forms.ChoiceField(choices=get_categories_for_mimes(
            Document.objects.active().filter(project=self.project).distinct('mime').order_by('mime').values_list(
                'mime')), widget=forms.Select(attrs={'class': 'span3'}))


class DeleteProjectsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DeleteProjectsForm, self).__init__(*args, **kwargs)

        choices = []
        for company in Company.objects.active().filter(pk__in=Project.objects.deleted().values('company')):
            projects = [(project.pk, project.name) for project in Project.objects.deleted().filter(company=company)]
            choices.append((company.name, projects))

        self.fields['project'] = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'class': 'span3'}))

    def save(self):
        project = Project.objects.deleted().get(pk=self.cleaned_data['project'])
        project.set_active(True)
        return project


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company')
        self.is_admin = kwargs.pop('is_admin')
        super(ProjectForm, self).__init__(*args, **kwargs)
        if self.is_admin:
            self.fields['company'] = forms.ModelChoiceField(queryset=Company.objects.active(),
                                                            widget=forms.Select(attrs={'class': 'span3'}))

    class Meta:
        model = Project
        fields = ('name', 'company')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'span3'})
        }

    def save(self, commit=True):
        if self.is_admin:
            self.instance.owner = self.cleaned_data['company']
        else:
            self.instance.owner = self.company
        project = super(ProjectForm, self).save(commit)
        # Add all of the companies accounts to the project.
        #[self.instance.clients.add(person) for person in Person.active.filter(company=self.company)]
        return project


class SortForm(forms.Form):
    search = forms.ChoiceField(choices=(('DATE', 'Sort by Date'), ('AZ', 'Sort Alphabetically')),
                               widget=forms.RadioSelect,
                               initial='DATE')



