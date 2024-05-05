from django.urls import path
from django.contrib.auth.views import LoginView, logout_then_login
from django.urls import path, include

from .views import *

app_name='users'

urlpatterns = [
    path(
        '',
        view=UsersView.as_view(),
        name='users',
    ),

    path(
        'invite_user',
        view=InviteUserView.as_view(),
        name='invite_user',
    ),

    path(
        '<int:pk>/settings/details',
        view=DetailsView.as_view(),
        name='details',
    ),

    path(
        '<int:pk>/settings/avatar',
        view=AvatarView.as_view(),
        name='avatar',
    ),

    path(
        '<int:pk>/settings/password',
        view=PasswordView.as_view(),
        name='password',
    ),

    path(
       'login/',
       view=LoginView.as_view(redirect_authenticated_user=True, template_name='login.html'),
       name='login'
    ),

    path(
       'logout/',
       view=logout_then_login,
       kwargs={'login_url': '/accounts/login'},
       name='logout'
    ),

    path('', include('django.contrib.auth.urls')),

    path(
        'reset/<uidb64>/<token>',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),

    path(
        'export_download/<token>',
        ExportView.as_view(),
        name='download_export'
    ),
]
