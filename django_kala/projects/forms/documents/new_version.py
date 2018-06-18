from django import forms
from django.conf import settings

from documents.models import Document, DocumentVersion


class NewDocumentVersionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        self.user = kwargs.pop('user')
        self.document = kwargs.pop('document')
        super(NewDocumentVersionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DocumentVersion
        fields = ['description', 'file']

    def save(self, commit=True):
        self.instance.document = self.document
        self.instance.user = self.user
        manager = settings.PLATFORM_MANAGER()
        manager.upload_document(self.cleaned_data['file'].read(), str(self.instance.uuid))
        # TODO: Remove this when file uploading becomes more civilized.
        self.file = None

        return super(NewDocumentVersionForm, self).save(commit)
