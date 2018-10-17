from django import forms

from organizations.models import Organization


class TransferOwnershipForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        self.organizations = kwargs.pop('organizations')
        super(TransferOwnershipForm, self).__init__(*args, **kwargs)

        self.fields['organization'] = forms.ModelChoiceField(
            queryset=self.organizations,
            initial=self.project.organization,
            widget=forms.Select(attrs={'class': 'ui search dropdown'})
        )

    def save(self, commit=True):
        self.project.organization = self.cleaned_data['organization']
        if commit:
            self.project.save()
        return self.project
