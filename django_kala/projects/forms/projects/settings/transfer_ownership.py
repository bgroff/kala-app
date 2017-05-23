from django import forms

from companies.models import Company


class TransferOwnershipForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super(TransferOwnershipForm, self).__init__(*args, **kwargs)

        self.fields['company'] = forms.ModelChoiceField(
            queryset=Company.objects.active(),
            initial=self.project.company,
            widget=forms.Select(attrs={'class': 'ui search dropdown'})
        )

    def save(self, commit=True):
        self.project.company = self.cleaned_data['company']
        if commit:
            self.project.save()
        return self.project
