from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class InviteUserForm(forms.ModelForm):
    user_type = forms.ChoiceField(
        choices=[
            ['creator', _('Creator')],
            ['collaborator', _('Collaborator')],
            ['manager', _('Manager')]
        ]
    )

    class Meta:
        model = get_user_model()
        fields = ['email', 'organizations', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(InviteUserForm, self).__init__(*args, **kwargs)
        self.fields['organizations'].widget.attrs['class'] = 'ui fluid dropdown'
        self.fields['user_type'].widget.attrs['class'] = 'ui fluid dropdown'
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def save(self, commit=True):
        self.instance.is_active = False
        return super(InviteUserForm, self).save(commit=commit)
