from django import forms

from auth.models import Permissions
from django.contrib.auth.models import Permission


def manage_access_forms(request, document):
    add_document_permission = Permission.objects.get(codename='add_document')
    change_document_permission = Permission.objects.get(codename='change_document')
    delete_document_permission = Permission.objects.get(codename='delete_document')
    permissions = Permissions.objects.filter(
        object_uuid=document.uuid
    ).select_related(
        'permission',
        'user'
    )

    users = document.get_users(request.user)
    forms = []
    for user in users:
        forms.append(ManageAccessForm(
            request.POST or None,
            document=document,
            user=user,
            add_document=add_document_permission,
            change_document=change_document_permission,
            delete_document=delete_document_permission,
            permissions=permissions,
        ))
    return forms


class ManageAccessForm(forms.Form):
    def __init__(self, *args, **kwargs):

        self.add_document_permission = kwargs.pop('add_document')
        self.change_document_permission = kwargs.pop('change_document')
        self.delete_document_permission = kwargs.pop('delete_document')

        self.document = kwargs.pop('document')
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
        self.fields['add_document_{0}'.format(self.user.pk)] = forms.BooleanField(
            required=False,
            label='',
            initial=True if 'add_document' in self.permissions_dict.get(self.user.pk, []) else False,
            widget=forms.CheckboxInput(
                attrs={'pk': self.document.pk}
            )
        )
        self.fields['change_document_{0}'.format(self.user.pk)] = forms.BooleanField(
            required=False,
            label='',
            initial=True if 'change_document' in self.permissions_dict.get(self.user.pk, []) else False,
            widget=forms.CheckboxInput(
                attrs={'pk': self.document.pk}
            )
        )
        self.fields['delete_document_{0}'.format(self.user.pk)] = forms.BooleanField(
            required=False,
            label='',
            initial=True if 'delete_document' in self.permissions_dict.get(self.user.pk, []) else False,
            widget=forms.CheckboxInput(
                attrs={'pk': self.document.pk}
            )
        )

    def save(self):
        # TODO, this can be sped up by using the permissions dict.
        if self.cleaned_data['add_document_{0}'.format(self.user.pk)]:
            if 'add_document' not in self.permissions_dict.get(self.user.pk, []):
                Permissions.objects.create(
                    user=self.user,
                    permission=self.add_document_permission,
                    object_uuid=self.document.uuid
                )
        elif 'add_document' in self.permissions_dict.get(self.user.pk, []):
            Permissions.objects.filter(
                user=self.user,
                permission=self.add_document_permission,
                object_uuid=self.document.uuid
            ).delete()
        if self.cleaned_data['change_document_{0}'.format(self.user.pk)]:
            if 'change_document' not in self.permissions_dict.get(self.user.pk, []):
                Permissions.objects.create(
                    user=self.user,
                    permission=self.change_document_permission,
                    object_uuid=self.document.uuid
                )
        elif 'change_document' in self.permissions_dict.get(self.user.pk, []):
            Permissions.objects.filter(
                user=self.user,
                permission=self.change_document_permission,
                object_uuid=self.document.uuid
            ).delete()
        if self.cleaned_data['delete_document_{0}'.format(self.user.pk)]:
            if 'delete_document' not in self.permissions_dict.get(self.user.pk, []):
                Permissions.objects.create(
                    user=self.user,
                    permission=self.delete_document_permission,
                    object_uuid=self.document.uuid
                )
        elif 'delete_document' in self.permissions_dict.get(self.user.pk, []):
            Permissions.objects.filter(
                user=self.user,
                permission=self.delete_document_permission,
                object_uuid=self.document.uuid
            ).delete()
