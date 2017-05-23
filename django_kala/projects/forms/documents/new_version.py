from django import forms

from documents.models import Document, DocumentVersion


class NewDocumentVersionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        self.person = kwargs.pop('person')
        self.document = kwargs.pop('document')
        super(NewDocumentVersionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DocumentVersion
        fields = ['description', 'file']

    def save(self, commit=True):
        self.instance.document = self.document
        self.instance.person = self.person
        return super(NewDocumentVersionForm, self).save(commit)
