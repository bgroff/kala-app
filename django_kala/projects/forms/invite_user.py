from django import forms
from django.contrib.auth import get_user_model


class InviteUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        admin_permission = kwargs.pop('admin_permission')
        super(InviteUserForm, self).__init__(*args, **kwargs)
        if admin_permission:
            user_type_choice = [['User', 'User'], ['Admin', 'Admin']]
        else:
            user_type_choice = [['User', 'User']]

        self.fields['user_type'] = forms.ChoiceField(choices=user_type_choice)

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name']

    def save(self, commit=True):
        self.instance.is_active = False
        return super(InviteUserForm, self).save(commit=commit)
