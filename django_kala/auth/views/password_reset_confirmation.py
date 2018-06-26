from django.contrib.auth import login as auth_login
from django.contrib.auth.views import INTERNAL_RESET_SESSION_TOKEN, PasswordResetConfirmView as DjangoPasswordResetConfirmView


class PasswordResetConfirmView(DjangoPasswordResetConfirmView):

    def form_valid(self, form):
        user = form.save()
        user.is_active = True
        user.save()

        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)
