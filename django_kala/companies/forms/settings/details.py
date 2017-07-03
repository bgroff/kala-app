from django import forms

from companies.models import Company


class DetailsForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name',
            'address',
            'address1',
            'city',
            'state',
            'zip',
            'country',
            'phone',
            'website'
        ]
