from django import forms

from organizations.models import Organization


def manage_access_forms(request, project):
    client_ids = project.clients.all().values_list('id', flat=True)
    forms = [ManageAccessForm(request.POST or None, project=project, organization=project.organization, client_ids=client_ids)]
    for organization in Organization.objects.active().exclude(pk=project.organization.pk).prefetch_related('user_set'):
        forms.append(ManageAccessForm(request.POST or None, project=project, organization=organization, client_ids=client_ids))
    return forms


class ManageAccessForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        client_ids = kwargs.pop('client_ids')
        self.organization = kwargs.pop('organization')
        self.people = self.organization.user_set.all()
        super(ManageAccessForm, self).__init__(*args, **kwargs)
        self.fields[self.organization] = forms.BooleanField(required=False, label='Select/Unselect All',
                                                       widget=forms.CheckboxInput(
                                                           attrs={'class': 'organization_checkbox',
                                                                  'pk_id': self.organization.pk,
                                                           }))

        for person in self.people:
            self.fields['%i' % person.pk] = forms.BooleanField(required=False, label=str(person),
                                                               initial=True if person.pk in client_ids else False,
                                                               widget=forms.CheckboxInput(
                                                                   attrs={'pk': self.organization.pk}))

    def save(self):
        for person in self.people:
            is_selected = self.cleaned_data['%i' % person.pk]
            if is_selected:
                if not self.project.clients.filter(pk=person.pk).exists():
                    self.project.clients.add(person)
            else:
                if self.project.clients.filter(pk=person.pk).exists():
                    self.project.clients.remove(person)

