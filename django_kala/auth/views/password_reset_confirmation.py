from django.contrib.auth import login as auth_login
from django.contrib.auth.views import INTERNAL_RESET_SESSION_TOKEN, PasswordResetConfirmView as DjangoPasswordResetConfirmView
from django.urls import reverse_lazy


class PasswordResetConfirmView(DjangoPasswordResetConfirmView):
    success_url = reverse_lazy('users:password_reset_complete')

    def form_valid(self, form):
        user = form.save()
        user.is_active = True
        user.save()

        return super().form_valid(form)
