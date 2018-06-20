from django import forms
from django.contrib.auth import get_user_model


class InviteUserForm(forms.ModelForm):
    user_type = forms.ChoiceField(choices=[['User', 'User'], ['Admin', 'Admin']])

    class Meta:
        model = get_user_model()
        fields = ['email', 'organizations']
