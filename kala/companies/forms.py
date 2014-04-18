from django import forms
from .models import Company
from ..accounts.models import Person


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('is_active', 'removed')


class CreateCompanyForm(CompanyForm):
    class Meta:
        model = Company
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'span3'})
        }


class DeletedPeopleForm(forms.Form):
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(DeletedPeopleForm, self).__init__(*args, **kwargs)
        self.fields['person'] = forms.ModelChoiceField(queryset=Person.objects.filter(company=company, is_active=False),
                                                       widget=forms.Select(attrs={'class': 'span3'}))

    def save(self):
        person = self.cleaned_data['person']
        person.set_active(True)
        return person
