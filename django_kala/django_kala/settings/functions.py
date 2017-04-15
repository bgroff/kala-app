from django.core.exceptions import ImproperlyConfigured
import os


def get_env_variable(variable, default=None):
    try:
        return os.environ[variable]
    except KeyError:
        if default is not None:
            return default
        raise ImproperlyConfigured("The environment variable {0} is not set.".format(variable))
