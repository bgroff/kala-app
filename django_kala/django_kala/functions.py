from importlib import import_module

from django.core.exceptions import ImproperlyConfigured
import os


def get_env_variable(variable, default=None):
    try:
        return os.environ[variable]
    except KeyError:
        if default is not None:
            return default
        raise ImproperlyConfigured("The environment variable {0} is not set.".format(variable))


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        # Nod to tastypie's use of importlib.
        module_path, class_name = val.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = "Could not import '%s' for API setting '%s'. %s: %s." % (val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


def create_user_permissions(permissions, users):
    permissions_dict = {}
    for permission in permissions:
        try:
            permissions_dict[permission.user.pk].append(permission.permission.codename)
        except KeyError:
            permissions_dict[permission.user.pk] = [permission.permission.codename]
    users_list = []
    for user in users:
        state = 'none'
        try:
            if 'can_create' in permissions_dict[user.pk]:
                state = 'can_create'
        except KeyError:
            pass
        try:
            if 'can_invite' in permissions_dict[user.pk]:
                state = 'can_invite'
        except KeyError:
            pass
        try:
            if 'can_manage' in permissions_dict[user.pk]:
                state = 'can_manage'
        except KeyError:
            pass

        users_list.append(
            {
                'name': str(user),
                'id': user.pk,
                'state': state,

                'can_create': "True" if 'can_create' == state else "False",
                'can_invite': "True" if 'can_invite' == state else "False",
                'can_manage': "True" if 'can_manage' == state else "False",
            }
        )
    return users_list
