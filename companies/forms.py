from django import forms
from accounts.models import Person
from .models import Companies


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Companies
        exclude = ('is_active', 'removed')


class CreateCompanyForm(CompanyForm):
    class Meta:
        model = Companies
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'span3'})
        }


class DeletedPeopleForm(forms.Form):
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(DeletedPeopleForm, self).__init__(*args, **kwargs)
        self.fields['person'] = forms.ModelChoiceField(queryset=Person.deleted.filter(company=company),
                                                       widget=forms.Select(attrs={'class': 'span3'}))

    def save(self):
        person = self.cleaned_data['person']
        person.set_active(True)
        return person
