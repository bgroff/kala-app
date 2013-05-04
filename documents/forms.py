import datetime
from companies.models import Companies
from django import forms
from projects.models import Projects
from .models import DocumentVersion, Documents


class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        self.person = kwargs.pop('person')
        # If a document is passed, then this is a version.
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


class ProjectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.document = kwargs.pop('document')
        super(ProjectForm, self).__init__(*args, **kwargs)

        choices = []
        for company in Companies.with_projects.all():
            projects = [(project.pk, project.name) for project in company.get_project_list()]
            choices.append((company.name, projects))

        self.fields['project'] = forms.ChoiceField(choices=choices, initial=self.document.project.pk)

    def save(self):
        self.document.project_id = self.cleaned_data['project']
        self.document.save()
        return self.document
