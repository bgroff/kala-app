from companies.models import Companies
from django import forms
from kala.templatetags.kala_tags import pretty_user
from people.models import People
from .models import Projects


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company')
        self.is_admin = kwargs.pop('is_admin')
        super(ProjectForm, self).__init__(*args, **kwargs)
        if self.is_admin:
            self.fields['company'] = forms.ModelChoiceField(queryset=Companies.active.all(), initial=self.company)

    class Meta:
        model = Projects
        exclude = ['owner', 'additional_companies', 'clients', 'created', 'changed', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'span3'})
        }

    def save(self, commit=True):
        if self.is_admin:
            self.instance.owner = self.cleaned_data['company']
        else:
            self.instance.owner = self.company
        project = super(ProjectForm, self).save(commit)
        # Add all of the companies people to the project.
        [self.instance.clients.add(person) for person in People.active.filter(company=self.company)]
        return project


def permission_forms(request, project):
    forms = [PermissionsForm(request.POST or None, project=project, company=project.company)]
    for company in Companies.active.all().exclude(pk=project.company.pk):
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
