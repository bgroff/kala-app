import datetime
from django import forms
from documents.models import Person, DocumentVersion, Document, Project, Company
from documents.templatetags.kala_tags import pretty_user


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ['last_updated', 'company', 'avatar_url', 'is_staff', 'is_active', 'date_joined', 'is_superuser',
                   'groups', 'user_permissions', 'password', 'last_login', 'username', 'access_new_projects',
                   'is_admin', 'username', 'timezone'] #timezone should not be ignored

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)

    password = forms.CharField(required=False, widget=forms.PasswordInput())
    confirm = forms.CharField(required=False, widget=forms.PasswordInput())

    def clean_confirm(self):
        password = self.cleaned_data['password']
        confirm = self.cleaned_data['confirm']
        if confirm != password:
            raise forms.ValidationError("The two passwords do not exists.")
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
        del self.fields['password'];
        del self.fields['confirm']

    class Meta:
        model = Person
        exclude = ['title', 'timezone', 'fax', 'home', 'mobile', 'office', 'ext', 'im_handle', 'im_service',
                   'last_updated', 'avatar_url', 'is_staff', 'is_active', 'date_joined', 'is_superuser', 'groups',
                   'user_permissions', 'password', 'confirm', 'last_login', 'username', 'access_new_projects',
                   'is_admin',
        ]

    def clean_email(self):
        try:
            Person.active.get(username=self.cleaned_data['email'])
            raise forms.ValidationError("This email is already in use.")
        except Person.DoesNotExist:
            return self.cleaned_data['email']

    def save(self, *args, **kwargs):
        self.instance.set_unusable_password()
        self.instance.is_active = True
        self.instance.company = self.cleaned_data['company']
        return super(CreatePersonForm, self).save(*args, **kwargs)


class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        self.person = kwargs.pop('person')
        try:
            self.document = kwargs.pop('document')
        except KeyError:
            self.document = None
        super(DocumentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DocumentVersion
        exclude = ['uuid', 'document', 'created', 'changed', 'mime', 'person', 'name']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'span3'})
        }

    def save(self, *args, **kwargs):
        now = datetime.datetime.now()
        if self.document is None:
            self.document = Document.active.create(project=self.project, date=now)
        self.instance.project = self.project
        self.instance.person = self.person
        self.instance.document = self.document
        self.instance.mime = self.cleaned_data['file'].content_type
        self.instance.name = self.cleaned_data['file'].name
        self.instance.created = now
        return super(DocumentForm, self).save(*args, **kwargs)


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company')
        self.is_admin = kwargs.pop('is_admin')
        super(ProjectForm, self).__init__(*args, **kwargs)
        if self.is_admin:
            self.fields['company'] = forms.ModelChoiceField(queryset=Company.active.all(), initial=self.company)

    class Meta:
        model = Project
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
        [self.instance.clients.add(person) for person in Person.active.filter(company=self.company)]
        return project


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['is_active']


class CreateCompanyForm(CompanyForm):
    class Meta:
        model = Company
        exclude = ['address', 'address1', 'city', 'state', 'zip', 'country', 'fax', 'phone', 'locale', 'timezone',
                   'website', 'is_active']


def permission_forms(request, project):
    forms = [PermissionsForm(request.POST or None, project=project, company=project.owner)]
    for company in Company.active.all().exclude(pk=project.owner.pk):
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
