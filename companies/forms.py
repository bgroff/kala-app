from django import forms
from .models import Companies


# Use fields instead of exclude
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Companies
        exclude = ['is_active']


class CreateCompanyForm(CompanyForm):
    class Meta:
        model = Companies
        exclude = ['address', 'address1', 'city', 'state', 'zip', 'country', 'fax', 'phone', 'locale', 'timezone',
                   'website', 'is_active']

