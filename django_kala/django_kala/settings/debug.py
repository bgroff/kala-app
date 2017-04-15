from .functions import get_env_variable

# SECURITY WARNING: don't run with debug turned on in production!
deployment = get_env_variable('DEPLOYMENT', True)
if type(deployment) is str:
    if deployment == 'production':
        DEBUG = False
    else:
        DEBUG = True
else:
    DEBUG = True
