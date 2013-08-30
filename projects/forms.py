from companies.models import Company
from django import forms
from documents.defs import get_categories_for_mimes
from documents.models import Document
from kala.templatetags.kala_tags import pretty_user
from .models import Project


class CategoryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super(CategoryForm, self).__init__(*args, **kwargs)

        self.fields['category'] = forms.ChoiceField(choices=get_categories_for_mimes(
            Document.objects.active().filter(project=self.project).distinct('mime').order_by('mime').values_list(
                'mime')), widget=forms.Select(attrs={'class': 'span3'}))


class CompanyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super(CompanyForm, self).__init__(*args, **kwargs)

        self.fields['company'] = forms.ModelChoiceField(queryset=Company.objects.active(),
                                                        initial=self.project.company,
                                                        widget=forms.Select(attrs={'class': 'span3'}))

    def save(self):
        self.project.company = self.cleaned_data['company']
        self.project.save()
        return self.project


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


def permission_forms(request, project):
    forms = [PermissionsForm(request.POST or None, project=project, company=project.company)]
    for company in Company.objects.active().exclude(pk=project.company.pk):
        forms.append(PermissionsForm(request.POST or None, project=project, company=company))
    return forms


class PermissionsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        self.company = kwargs.pop('company')
        self.people = self.company.get_people_list()
        super(PermissionsForm, self).__init__(*args, **kwargs)
        self.fields[self.company] = forms.BooleanField(required=False, label='Select/Unselect All',
                                                       widget=forms.CheckboxInput(
                                                           attrs={'class': 'company_checkbox',
                                                                  'pk_id': self.company.pk,
                                                           }))

        for person in self.people:
            self.fields['%i' % person.pk] = forms.BooleanField(required=False, label=pretty_user(person),
                                                               initial=True if self.project.clients.filter(
                                                                   pk=person.pk).exists() else False,
                                                               widget=forms.CheckboxInput(
                                                                   attrs={'pk': self.company.pk}))

    def save(self):
        for person in self.people:
            is_selected = self.cleaned_data['%i' % person.pk]
            if is_selected:
                if not self.project.clients.filter(pk=person.pk).exists():
                    self.project.clients.add(person)
            else:
                if self.project.clients.filter(pk=person.pk).exists():
                    self.project.clients.remove(person)


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company')
        self.is_admin = kwargs.pop('is_admin')
        super(ProjectForm, self).__init__(*args, **kwargs)
        if self.is_admin:
            self.fields['company'] = forms.ModelChoiceField(queryset=Company.objects.active(), initial=self.company,
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



