from django import forms

from organizations.models import Organization


class DetailsForm(forms.ModelForm):
    class Meta:
        model = Organization
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
