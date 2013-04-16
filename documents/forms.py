import datetime
from django import forms
from .models import DocumentVersion, Documents


class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        self.person = kwargs.pop('person')
        try:
            self.document = kwargs.pop('document')
        except KeyError:
            self.document = None
        super(DocumentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DocumentVersion
        fields = ('file', 'description')
        widgets = {
            'description': forms.TextInput(attrs={'class': 'span3'})
        }

    def save(self, *args, **kwargs):
        now = datetime.datetime.now()
        if self.document is None:
            self.document = Documents.objects.create(project=self.project, date=now)
        self.instance.project = self.project
        self.instance.person = self.person
        self.instance.document = self.document
        self.instance.mime = self.cleaned_data['file'].content_type
        self.instance.name = self.cleaned_data['file'].name
        self.instance.created = now
        return super(DocumentForm, self).save(*args, **kwargs)
