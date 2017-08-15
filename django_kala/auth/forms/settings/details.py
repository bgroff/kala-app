from django import forms
from django.contrib.auth import get_user_model


class DetailsForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'email',
            'title',
            'timezone',
            'mobile',
            'office'
        ]
