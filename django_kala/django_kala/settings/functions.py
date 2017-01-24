from django.core.exceptions import ImproperlyConfigured
import os


def get_env_variable(variable):
    try:
        return os.environ[variable]
    except KeyError:
        raise ImproperlyConfigured("The environment variable {0} is not set.".format(variable))
