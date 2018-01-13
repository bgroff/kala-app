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

