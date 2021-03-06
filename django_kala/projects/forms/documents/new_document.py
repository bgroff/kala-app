from django import forms
from django.conf import settings

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
        self.user = kwargs.pop('user')
        super(NewDocumentVersionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DocumentVersion
        fields = ['description', 'file']

    def save(self, document, commit=True):
        self.instance.document = document
        self.instance.user = self.user
        manager = settings.PLATFORM_MANAGER()
        manager.upload_document(self.cleaned_data['file'].read(), str(self.instance.uuid))
        # TODO: Remove this when file uploading becomes more civilized.
        self.file = None

        return super(NewDocumentVersionForm, self).save(commit)
