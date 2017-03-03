from django.core.exceptions import ImproperlyConfigured
import os


def get_env_variable(variable, default=None):
    try:
        if default is None:
            return os.environ[variable]
        return default
    except KeyError:
        raise ImproperlyConfigured("The environment variable {0} is not set.".format(variable))
