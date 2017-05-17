from django import forms

from projects.models import Project


class DetailsForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'tags']
