from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())


class AdminRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        user = get_user(request)
        if not user.is_admin:
            raise PermissionDenied()
        return super(AdminRequiredMixin, self).dispatch(request, *args, **kwargs)
