from django import forms

from projects.models import Project


class NewProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.organizations = kwargs.pop('organizations')
        super(NewProjectForm, self).__init__(*args, **kwargs)
        self.fields['organization'] = forms.ModelChoiceField(
            queryset=self.organizations,
            widget=forms.Select(attrs={'class': 'ui search dropdown', 'required': 'true'})
        )

    class Meta:
        model = Project
        fields = ['name', 'description', 'tags', 'organization']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Project name'}),
            'description': forms.Textarea(
                attrs={'placeholder': 'Project description'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Comma separated tags'})
        }
