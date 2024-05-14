from django_kala.functions import get_env_variable

AUTHENTICATION_METHOD = get_env_variable('KALA_AUTHENTICATION_METHOD', default="oidc")

if AUTHENTICATION_METHOD == "oidc":

    AUTHENTICATION_BACKENDS = [
        'mozilla_django_oidc.auth.OIDCAuthenticationBackend',
    ]
    OIDC_OP_AUTHORIZATION_ENDPOINT = get_env_variable(
        "OIDC_OP_AUTHORIZATION_ENDPOINT",
    )
    OIDC_OP_TOKEN_ENDPOINT = get_env_variable(
        "OIDC_OP_TOKEN_ENDPOINT",
    )
    OIDC_OP_USER_ENDPOINT = get_env_variable(
        "OIDC_OP_USER_ENDPOINT",
    )
    OIDC_OP_JWKS_ENDPOINT = get_env_variable(
        "OIDC_OP_JWKS_ENDPOINT",
    )
    OIDC_OP_LOGOUT_ENDPOINT = get_env_variable(
        "OIDC_OP_LOGOUT_ENDPOINT",
    )
    OIDC_RP_SIGN_ALGO = get_env_variable(
        "OIDC_RP_SIGN_ALGO",
        default="RS256"
    )

    OIDC_RP_CLIENT_ID = get_env_variable(
        "OIDC_RP_CLIENT_ID",
    )
    OIDC_RP_CLIENT_SECRET = get_env_variable(
        "OIDC_RP_CLIENT_SECRET",
    )
    OIDC_CREATE_USER = True

    ALLOW_LOGOUT_GET_METHOD = True

    LOGIN_REDIRECT_URL = '/'
    LOGIN_REDIRECT_URL_FAILURE = 'https://google.com'
    LOGIN_URL = '/oidc/authenticate/'
    LOGOUT_REDIRECT_URL = OIDC_OP_LOGOUT_ENDPOINT
else:
    LOGIN_REDIRECT_URL = '/'
    LOGIN_URL = '/accounts/login'
