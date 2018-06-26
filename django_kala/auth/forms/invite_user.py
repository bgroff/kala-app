from django import forms
from django.contrib.auth import get_user_model


class InviteUserForm(forms.ModelForm):
    user_type = forms.ChoiceField(choices=[['User', 'User'], ['Admin', 'Admin']])

    class Meta:
        model = get_user_model()
        fields = ['email', 'organizations', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(InviteUserForm, self).__init__(*args, **kwargs)
        self.fields['organizations'].widget.attrs['class'] = 'ui fluid dropdown'
        self.fields['user_type'].widget.attrs['class'] = 'ui fluid dropdown'

    def save(self, commit=True):
        self.instance.is_active = False
        return super(InviteUserForm, self).save(commit=commit)
