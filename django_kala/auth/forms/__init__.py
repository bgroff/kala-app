from .settings.details import DetailsForm
from .invite_user import InviteUserForm


from django import forms
from django.contrib.auth import get_user_model

from organizations.models import Organization
from projects.models import Project


class PersonForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            'first_name', 'last_name', 'email', 'title'
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'span3'})
        }

    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'span3'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'span3'}))
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'span3'}))

    new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'span3'}))
    confirm = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'span3'}))

    def clean_confirm(self):
        password = self.cleaned_data['new_password']
        confirm = self.cleaned_data['confirm']
        if confirm != password:
            raise forms.ValidationError("The two passwords do not match.")
        if confirm != '':
            self.confirm = confirm
        return confirm

    def save(self, commit=True, *args, **kwargs):
        if hasattr(self, 'confirm'):
            self.instance.set_password(self.confirm)
        return super(PersonForm, self).save(commit, *args, **kwargs)


class CreatePersonForm(PersonForm):
    def __init__(self, *args, **kwargs):
        super(CreatePersonForm, self).__init__(*args, **kwargs)
        del self.fields['new_password']
        del self.fields['confirm']

    organizations = forms.ModelChoiceField(queryset=Organization.objects.active(), widget=forms.Select(attrs={'class': 'span3'}))

    class Meta:
        model = get_user_model()
        fields = (
            'email', 'first_name', 'last_name', 'organizations'
        )

    def clean_email(self):
        try:
            get_user_model().objects.get(username=self.cleaned_data['email'])
            raise forms.ValidationError("This email is already in use.")
        except get_user_model().DoesNotExist:
            return self.cleaned_data['email']

    def save(self, *args, **kwargs):
        self.instance.username = self.cleaned_data['email']
        self.instance.set_unusable_password()
        self.instance.is_active = True
        self.instance.Organization = self.cleaned_data['prganization']
        return super(CreatePersonForm, self).save(*args, **kwargs)


class DeletedCompanyForm(forms.Form):
    organization = forms.ModelChoiceField(queryset=Organization.objects.deleted(),
                                     widget=forms.Select(attrs={'class': 'span3'}))

    def save(self):
        organization = self.cleaned_data['organization']
        organization.set_active(True)
        return organization


def permission_forms(request, person):
    return [PermissionsForm(request.POST or None, person=person, organization=organization) for organization in
            Organization.objects.active().filter(pk__in=Project.objects.active().values('organization__pk'))]


class PermissionsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.person = kwargs.pop('person')
        self.organization = kwargs.pop('organization')
        self.projects = Project.objects.active().filter(organization=self.organization)
        super(PermissionsForm, self).__init__(*args, **kwargs)
        self.fields[self.organization] = forms.BooleanField(required=False, label='Select/Unselect All',
                                                       widget=forms.CheckboxInput(
                                                           attrs={'class': 'organization_checkbox',
                                                                  'pk_id': self.organization.pk,
                                                           }))
        for project in self.projects:
            self.fields['%i' % project.pk] = forms.BooleanField(required=False, label=project,
                                                                initial=True if project.clients.filter(
                                                                    pk=self.person.pk).exists() else False,
                                                                widget=forms.CheckboxInput(
                                                                    attrs={'pk': self.organization.pk}))

    def save(self):
        for project in self.projects:
            is_selected = self.cleaned_data['%i' % project.pk]
            if is_selected:
                if not project.clients.filter(pk=self.person.pk).exists():
                    project.clients.add(self.person)
            else:
                if project.clients.filter(pk=self.person.pk).exists():
                    project.clients.remove(self.person)
