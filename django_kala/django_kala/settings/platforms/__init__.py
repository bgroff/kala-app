from ..functions import get_env_variable, import_from_string

PLATFORM = get_env_variable('PLATFORM', default='local')
if PLATFORM == 'local':
    from .local import *
elif PLATFORM == 'aws':
    from .aws import *

PLATFORM_MANAGER = import_from_string(
    'django_kala.platforms.{0}.manager.PlatformManager'.format(PLATFORM),
    'PLATFORM_MANAGER'
)
