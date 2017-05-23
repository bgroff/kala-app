from django import forms

from documents.models import Document, DocumentVersion


class NewDocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super(NewDocumentForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(
            queryset=self.project.category_set.all(),
            widget=forms.Select(attrs={'class': 'ui search dropdown'}),
            required=False
        )

    class Meta:
        model = Document
        fields = ['category', 'tags']

    def save(self, commit=True):
        self.instance.project = self.project
        return super(NewDocumentForm, self).save(commit)


class NewDocumentVersionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        self.person = kwargs.pop('person')
        super(NewDocumentVersionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DocumentVersion
        fields = ['description', 'file']

    def save(self, document, commit=True):
        self.instance.document = document
        self.instance.person = self.person
        return super(NewDocumentVersionForm, self).save(commit)
