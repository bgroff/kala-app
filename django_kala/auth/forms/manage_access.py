from django import forms

from django.contrib.auth.models import Permission


def manage_access_forms(request, obj, permission_class, field):
    forms = []

    can_create = Permission.objects.get(codename='can_create', content_type__app_label='{0}s'.format(field))
    can_invite = Permission.objects.get(codename='can_invite', content_type__app_label='{0}s'.format(field))
    can_manage = Permission.objects.get(codename='can_manage', content_type__app_label='{0}s'.format(field))

    users = request.user.get_users()
    permissions = permission_class.objects.filter(**{
            field: obj,
            "user__in": users
    }).select_related(
        'permission',
        'user'
    )

    for user in users:
        forms.append(ManageAccessForm(
            request.POST or None,
            obj=obj,
            user=user,
            can_create=can_create,
            can_invite=can_invite,
            can_manage=can_manage,
            permissions=permissions,
        ))
    return forms


class ManageAccessForm(forms.Form):
    def __init__(self, *args, **kwargs):

        self.can_create = kwargs.pop('can_create')
        self.can_invite = kwargs.pop('can_invite')
        self.can_manage = kwargs.pop('can_manage')

        self.obj = kwargs.pop('obj')
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
        self.fields['can_create_{0}'.format(self.user.pk)] = forms.BooleanField(
            required=False,
            label='',
            initial=True if 'can_create' in self.permissions_dict.get(self.user.pk, []) else False,
            widget=forms.CheckboxInput(
                attrs={'pk': self.obj.pk}
            )
        )
        self.fields['can_invite_{0}'.format(self.user.pk)] = forms.BooleanField(
            required=False,
            label='',
            initial=True if 'can_invite' in self.permissions_dict.get(self.user.pk, []) else False,
            widget=forms.CheckboxInput(
                attrs={'pk': self.obj.pk}
            )
        )
        self.fields['can_manage_{0}'.format(self.user.pk)] = forms.BooleanField(
            required=False,
            label='',
            initial=True if 'can_manage' in self.permissions_dict.get(self.user.pk, []) else False,
            widget=forms.CheckboxInput(
                attrs={'pk': self.obj.pk}
            )
        )

    def save(self):
        if self.cleaned_data['can_create_{0}'.format(self.user.pk)]:
            if 'can_create' not in self.permissions_dict.get(self.user.pk, []):
                self.obj.add_create(self.user)
        elif 'can_create' in self.permissions_dict.get(self.user.pk, []):
            self.obj.delete_create(self.user)

        if self.cleaned_data['can_invite_{0}'.format(self.user.pk)]:
            if 'can_invite' not in self.permissions_dict.get(self.user.pk, []):
                self.obj.add_invite(self.user)
        elif 'can_invite' in self.permissions_dict.get(self.user.pk, []):
            self.obj.delete_invite(self.user)

        if self.cleaned_data['can_manage_{0}'.format(self.user.pk)]:
            if 'can_manage' not in self.permissions_dict.get(self.user.pk, []):
                self.obj.add_manage(self.user)
        elif 'can_manage' in self.permissions_dict.get(self.user.pk, []):
            self.obj.delete_manage(self.user)
