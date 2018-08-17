from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class EmailForm(forms.Form):
    email = forms.EmailField()


class InviteUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        admin_permission = kwargs.pop('admin_permission')
        super(InviteUserForm, self).__init__(*args, **kwargs)
        if admin_permission:
            user_type_choice = [['User', _('User')], ['Admin', _('Admin')]]
        else:
            user_type_choice = [['User', 'User']]

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['user_type'] = forms.ChoiceField(choices=user_type_choice)
        self.fields['user_type'].widget.attrs['class'] = 'ui fluid dropdown'

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']

    def save(self, commit=True):
        self.instance.is_active = False
        return super(InviteUserForm, self).save(commit=commit)
