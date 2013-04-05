from django import forms
from documents.models import Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ['title', 'timezone', 'fax', 'home', 'mobile', 'office', 'ext', 'im_handle', 'im_service',
                   'last_updated', 'avatar_url', 'is_staff', 'is_active', 'date_joined', 'is_superuser', 'groups',
                   'user_permissions', 'password', 'last_login', 'username', 'access_new_projects',
                   'bc_id']  # Remove bc_id when done.

    def save(self, *args, **kwargs):
        self.instance.username = self.cleaned_data['email']
        self.instance.access_new_projects = False  # Probably should just remove this
        self.instance.is_active = True
        self.instance.set_unusable_password()
        super(PersonForm, self).save(*args, **kwargs)
