from django import forms


class TransferOwnershipForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.document = kwargs.pop('document')
        self.projects = kwargs.pop('projects')
        super(TransferOwnershipForm, self).__init__(*args, **kwargs)

        self.fields['project'] = forms.ModelChoiceField(
            queryset=self.projects,
            initial=self.document.project,
            widget=forms.Select(attrs={'class': 'ui search dropdown'})
        )

    def save(self, commit=True):
        self.document.project = self.cleaned_data['project']
        if commit:
            self.document.save()
        return self.document
