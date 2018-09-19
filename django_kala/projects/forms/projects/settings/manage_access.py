from django import forms

from auth.models import Permissions
from django.contrib.auth.models import Permission


def manage_access_forms(request, project):
    add_project_permission = Permission.objects.get(codename='add_project')
    change_project_permission = Permission.objects.get(codename='change_project')
    delete_project_permission = Permission.objects.get(codename='delete_project')
    permissions = Permissions.objects.filter(
        object_uuid=project.uuid
    ).select_related(
        'permission',
        'user'
    )

    users = request.user.get_users()
    forms = []
    for user in users:
        forms.append(ManageAccessForm(
            request.POST or None,
            project=project,
            user=user,
            add_project=add_project_permission,
            change_project=change_project_permission,
            delete_project=delete_project_permission,
            permissions=permissions,
        ))
    return forms


class ManageAccessForm(forms.Form):
    def __init__(self, *args, **kwargs):

        self.add_project_permission = kwargs.pop('add_project')
        self.change_project_permission = kwargs.pop('change_project')
        self.delete_project_permission = kwargs.pop('delete_project')

        self.project = kwargs.pop('project')
        self.user = kwargs.pop('user')
        self.permissions_dict = {}
        for permission in kwargs.pop('permissions'):
            try:
                self.permissions_dict[permission.user.pk].append(permission.permission.codename)
            except KeyError:
                self.permissions_dict[permission.user.pk] = [permission.permission.codename]
        try:
            self.permissions_dict[self.user.pk]
        except KeyError:
            self.is_empty = True

        super(ManageAccessForm, self).__init__(*args, **kwargs)
        self.fields['add_project_{0}'.format(self.user.pk)] = forms.BooleanField(
            required=False,
            label='',
            initial=True if 'add_project' in self.permissions_dict.get(self.user.pk, []) else False,
            widget=forms.CheckboxInput(
                attrs={'pk': self.project.pk}
            )
        )
        self.fields['change_project_{0}'.format(self.user.pk)] = forms.BooleanField(
            required=False,
            label='',
            initial=True if 'change_project' in self.permissions_dict.get(self.user.pk, []) else False,
            widget=forms.CheckboxInput(
                attrs={'pk': self.project.pk}
            )
        )
        self.fields['delete_project_{0}'.format(self.user.pk)] = forms.BooleanField(
            required=False,
            label='',
            initial=True if 'delete_project' in self.permissions_dict.get(self.user.pk, []) else False,
            widget=forms.CheckboxInput(
                attrs={'pk': self.project.pk}
            )
        )

    def save(self):
        # TODO, this can be sped up by using the permissions dict.
        if self.cleaned_data['add_project_{0}'.format(self.user.pk)]:
            if 'add_project' not in self.permissions_dict.get(self.user.pk, []):
                Permissions.objects.create(
                    user=self.user,
                    permission=self.add_project_permission,
                    object_uuid=self.project.uuid
                )
        elif 'add_project' in self.permissions_dict.get(self.user.pk, []):
            Permissions.objects.filter(
                user=self.user,
                permission=self.add_project_permission,
                object_uuid=self.project.uuid
            ).delete()
        if self.cleaned_data['change_project_{0}'.format(self.user.pk)]:
            if 'change_project' not in self.permissions_dict.get(self.user.pk, []):
                Permissions.objects.create(
                    user=self.user,
                    permission=self.change_project_permission,
                    object_uuid=self.project.uuid
                )
        elif 'change_project' in self.permissions_dict.get(self.user.pk, []):
            Permissions.objects.filter(
                user=self.user,
                permission=self.change_project_permission,
                object_uuid=self.project.uuid
            ).delete()
        if self.cleaned_data['delete_project_{0}'.format(self.user.pk)]:
            if 'delete_project' not in self.permissions_dict.get(self.user.pk, []):
                Permissions.objects.create(
                    user=self.user,
                    permission=self.delete_project_permission,
                    object_uuid=self.project.uuid
                )
        elif 'delete_project' in self.permissions_dict.get(self.user.pk, []):
            Permissions.objects.filter(
                user=self.user,
                permission=self.delete_project_permission,
                object_uuid=self.project.uuid
            ).delete()
