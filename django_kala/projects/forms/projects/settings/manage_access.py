from django import forms

from companies.models import Company


def manage_access_forms(request, project):
    client_ids = project.clients.all().values_list('id', flat=True)
    forms = [ManageAccessForm(request.POST or None, project=project, company=project.company, client_ids=client_ids)]
    for company in Company.objects.active().exclude(pk=project.company.pk).prefetch_related('user_set'):
        forms.append(ManageAccessForm(request.POST or None, project=project, company=company, client_ids=client_ids))
    return forms


class ManageAccessForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        client_ids = kwargs.pop('client_ids')
        self.company = kwargs.pop('company')
        self.people = self.company.user_set.all()
        super(ManageAccessForm, self).__init__(*args, **kwargs)
        self.fields[self.company] = forms.BooleanField(required=False, label='Select/Unselect All',
                                                       widget=forms.CheckboxInput(
                                                           attrs={'class': 'company_checkbox',
                                                                  'pk_id': self.company.pk,
                                                           }))

        for person in self.people:
            self.fields['%i' % person.pk] = forms.BooleanField(required=False, label=str(person),
                                                               initial=True if person.pk in client_ids else False,
                                                               widget=forms.CheckboxInput(
                                                                   attrs={'pk': self.company.pk}))

    def save(self):
        for person in self.people:
            is_selected = self.cleaned_data['%i' % person.pk]
            if is_selected:
                if not self.project.clients.filter(pk=person.pk).exists():
                    self.project.clients.add(person)
            else:
                if self.project.clients.filter(pk=person.pk).exists():
                    self.project.clients.remove(person)

