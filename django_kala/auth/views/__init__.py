from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from .settings.details import DetailsView
from .invite_user import InviteUserView
from .users import UsersView

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from ..forms.invite_user import InviteUserForm
from ..forms import PersonForm, permission_forms


class EditProfile(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = {
            'form': self.form,
            'user': self.user,
        }
        if self.request.user.c:
            context['permission_forms'] = self.permission_forms
        return context

    def dispatch(self, request, pk, *args, **kwargs):
        self.user = get_object_or_404(get_user_model(), pk=pk)
        if self.user != request.user and not request.user.is_superuser:
            messages.error(request, 'You do not have permission to edit this users account')
            return redirect(reverse('home'))
        self.form = PersonForm(request.POST or None, instance=self.user)
        if request.user.is_superuser:
            self.permission_forms = permission_forms(request, self.user)
        return super(EditProfile, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'toggle-admin' in request.POST and request.user.is_superuser:
            self.user.is_superuser = not self.user.is_superuser
            self.user.save()
            if self.user.is_superuser:
                messages.success(request, 'This user has been granted administrator privileges')
            else:
                messages.success(request, 'This user has had it\'s administrator privileges revoked')
            return redirect(reverse('edit_profile', args=[self.user.pk]))

        if 'delete' in request.POST and request.user.is_superuser:
            self.user.set_active(False)
            messages.success(request, 'The user has been removed')
            return redirect(reverse('accounts'))

        if 'save-permissions' in request.POST:
            for form in self.permission_forms:
                if form.is_valid():
                    form.save()
            messages.success(request, 'The permissions have been updated')
            return redirect(reverse('edit_profile', args=[self.user.pk]))

        if self.form.is_valid():
            self.form.save()
            messages.success(request, 'Profile data has been saved')
            return redirect(reverse('edit_profile', args=[self.user.pk]))
        return self.render_to_response(self.get_context_data())
