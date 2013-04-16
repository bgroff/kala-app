from django import forms
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
            'email', 'first_name', 'last_name'
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

