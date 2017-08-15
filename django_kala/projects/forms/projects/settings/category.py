from django import forms

from projects.models import Category


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super(CategoryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Category
        fields = ['name']

    def save(self, commit=True):
        self.instance.project = self.project
        super(CategoryForm, self).save(commit)
