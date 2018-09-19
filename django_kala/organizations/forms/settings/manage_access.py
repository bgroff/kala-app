from django import forms

from auth.models import Permissions
from django.contrib.auth.models import Permission


def manage_access_forms(request, organization):
    add_organization_permission = Permission.objects.get(codename='add_organization')
    change_organization_permission = Permission.objects.get(codename='change_organization')
    delete_organization_permission = Permission.objects.get(codename='delete_organization')
    permissions = Permissions.objects.filter(
        object_uuid=organization.uuid
    ).select_related(
        'permission',
        'user'
    )

    users = request.user.get_users()
    forms = []
    for user in users:
        forms.append(ManageAccessForm(
            request.POST or None,
            organization=organization,
            user=user,
            add_organization=add_organization_permission,
            change_organization=change_organization_permission,
            delete_organization=delete_organization_permission,
            permissions=permissions,
        ))
    return forms


class ManageAccessForm(forms.Form):
    def __init__(self, *args, **kwargs):

        self.add_organization_permission = kwargs.pop('add_organization')
        self.change_organization_permission = kwargs.pop('change_organization')
        self.delete_organization_permission = kwargs.pop('delete_organization')

        self.organization = kwargs.pop('organization')
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
        self.fields['add_organization_{0}'.format(self.user.pk)] = forms.BooleanField(
            required=False,
            label='',
            initial=True if 'add_organization' in self.permissions_dict.get(self.user.pk, []) else False,
            widget=forms.CheckboxInput(
                attrs={'pk': self.organization.pk}
            )
        )
        self.fields['change_organization_{0}'.format(self.user.pk)] = forms.BooleanField(
            required=False,
            label='',
            initial=True if 'change_organization' in self.permissions_dict.get(self.user.pk, []) else False,
            widget=forms.CheckboxInput(
                attrs={'pk': self.organization.pk}
            )
        )
        self.fields['delete_organization_{0}'.format(self.user.pk)] = forms.BooleanField(
            required=False,
            label='',
            initial=True if 'delete_organization' in self.permissions_dict.get(self.user.pk, []) else False,
            widget=forms.CheckboxInput(
                attrs={'pk': self.organization.pk}
            )
        )

    def save(self):
        # TODO, this can be sped up by using the permissions dict.
        if self.cleaned_data['add_organization_{0}'.format(self.user.pk)]:
            if 'add_organization' not in self.permissions_dict.get(self.user.pk, []):
                Permissions.objects.create(
                    user=self.user,
                    permission=self.add_organization_permission,
                    object_uuid=self.organization.uuid
                )
        elif 'add_organization' in self.permissions_dict.get(self.user.pk, []):
            Permissions.objects.filter(
                user=self.user,
                permission=self.add_organization_permission,
                object_uuid=self.organization.uuid
            ).delete()
        if self.cleaned_data['change_organization_{0}'.format(self.user.pk)]:
            if 'change_organization' not in self.permissions_dict.get(self.user.pk, []):
                Permissions.objects.create(
                    user=self.user,
                    permission=self.change_organization_permission,
                    object_uuid=self.organization.uuid
                )
        elif 'change_organization' in self.permissions_dict.get(self.user.pk, []):
            Permissions.objects.filter(
                user=self.user,
                permission=self.change_organization_permission,
                object_uuid=self.organization.uuid
            ).delete()
        if self.cleaned_data['delete_organization_{0}'.format(self.user.pk)]:
            if 'delete_organization' not in self.permissions_dict.get(self.user.pk, []):
                Permissions.objects.create(
                    user=self.user,
                    permission=self.delete_organization_permission,
                    object_uuid=self.organization.uuid
                )
        elif 'delete_organization' in self.permissions_dict.get(self.user.pk, []):
            Permissions.objects.filter(
                user=self.user,
                permission=self.delete_organization_permission,
                object_uuid=self.organization.uuid
            ).delete()
