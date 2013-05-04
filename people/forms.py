from django import forms
from companies.models import Companies
from projects.models import Projects
from .models import People


class PersonForm(forms.ModelForm):
    class Meta:
        model = People
        fields = (
            'first_name', 'last_name', 'email', 'title', 'password', 'confirm',
        )

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)

    password = forms.CharField(required=False, widget=forms.PasswordInput())
    confirm = forms.CharField(required=False, widget=forms.PasswordInput())

    def clean_confirm(self):
        password = self.cleaned_data['password']
        confirm = self.cleaned_data['confirm']
        if confirm != password:
            raise forms.ValidationError("The two passwords do not match.")
        return confirm

    def save(self, commit=True, *args, **kwargs):
        self.instance.username = self.cleaned_data['email']
        self.instance.access_new_projects = False  # Probably should just remove this
        if hasattr(self, 'confirm') and self.cleaned_data['confirm']:
            self.instance.set_password(self.cleaned_data['confirm'])
        return super(PersonForm, self).save(commit, *args, **kwargs)


class CreatePersonForm(PersonForm):
    def __init__(self, *args, **kwargs):
        super(CreatePersonForm, self).__init__(*args, **kwargs)
        del self.fields['password']
        del self.fields['confirm']

    class Meta:
        model = People
        fields = (
            'email', 'first_name', 'last_name', 'company'
        )

    def clean_email(self):
        try:
            People.active.get(username=self.cleaned_data['email'])
            raise forms.ValidationError("This email is already in use.")
        except People.DoesNotExist:
            return self.cleaned_data['email']

    def save(self, *args, **kwargs):
        self.instance.set_unusable_password()
        self.instance.is_active = True
        self.instance.company = self.cleaned_data['company']
        return super(CreatePersonForm, self).save(*args, **kwargs)


class DeletedCompanyForm(forms.Form):
    company = forms.ModelChoiceField(queryset=Companies.deleted.all())

    def save(self):
        company = self.cleaned_data['company']
        company.set_active(True)
        return company


def permission_forms(request, person):
    return [PermissionsForm(request.POST or None, person=person, company=company) for company in
            Companies.active.filter(pk__in=Projects.active.all().values('company__pk'))]


class PermissionsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.person = kwargs.pop('person')
        self.company = kwargs.pop('company')
        self.projects = Projects.active.filter(company=self.company)
        super(PermissionsForm, self).__init__(*args, **kwargs)
        self.fields[self.company] = forms.BooleanField(required=False, label='Select/Unselect All',
                                                       widget=forms.CheckboxInput(
                                                           attrs={'class': 'company_checkbox',
                                                                  'pk_id': self.company.pk,
                                                           }))
        for project in self.projects:
            self.fields['%i' % project.pk] = forms.BooleanField(required=False, label=project,
                                                                initial=True if project.clients.filter(
                                                                    pk=self.person.pk).exists() else False,
                                                                widget=forms.CheckboxInput(
                                                                    attrs={'pk': self.company.pk}))

    def save(self):
        for project in self.projects:
            is_selected = self.cleaned_data['%i' % project.pk]
            if is_selected:
                if not project.clients.filter(pk=self.person.pk).exists():
                    project.clients.add(self.person)
            else:
                if project.clients.filter(pk=self.person.pk).exists():
                    project.clients.remove(self.person)
