from django import forms

from documents.models import Document


class DetailsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super(DetailsForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(
            queryset=self.project.category_set.all(),
            widget=forms.Select(attrs={'class': 'ui search dropdown'})
        )

    class Meta:
        model = Document
        fields = ['name', 'category', 'tags']
