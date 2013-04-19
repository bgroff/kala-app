from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import requests


class BasecampAuthorizationForm(forms.Form):
    name = forms.CharField(label="Basecamp Company Name", required=True)
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean(self):
        cleaned_data = super(BasecampAuthorizationForm, self).clean()
        url = 'https://%s.basecamphq.com' % cleaned_data['name']
        r = requests.get('%s/account.xml' % url, auth=(cleaned_data['username'], cleaned_data['password']))
        if r.status_code != 200:
            raise ValidationError("Basecamp failed to authorize your account information. Please check that the "
                                  "information you provided above is correct. The status code returned was %i"
                                  % r.status_code)
        return self.cleaned_data
