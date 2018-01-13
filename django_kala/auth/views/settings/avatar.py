from django.conf import settings

from auth.forms.settings.avatar import AvatarForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from PIL import Image
from io import BytesIO

size = 32, 32


class AvatarView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/settings/avatar.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'user': self.user,
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.user = get_object_or_404(get_user_model().objects.all(), pk=pk)

        if not request.user.is_superuser and request.user != self.user:
            raise PermissionDenied('You do not have permission to edit this user.')

        self.form = AvatarForm(request.POST or None, request.FILES or None)
        return super(AvatarView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            try:
                avatar_content = request.FILES['avatar'].read()
                avatar = Image.open(BytesIO(avatar_content))
                avatar = avatar.resize(size)
                avatar_out = BytesIO()
                avatar.save(avatar_out, format='PNG')
                avatar_out.seek(0)

                manager = settings.PLATFORM_MANAGER()
                manager.upload_avatar(avatar_out, self.user)

            except Exception as exception:
                print(exception)
            return redirect(reverse('users:avatar', args=[self.user.pk]))
        return self.render_to_response(self.get_context_data())


