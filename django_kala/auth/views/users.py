from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from organizations.models import Organization


class UsersView(LoginRequiredMixin, TemplateView):
    template_name = 'users.html'

    def get_context_data(self, **kwargs):
        users = self.request.user.get_users()
        organizations = self.request.user.get_organizations()

        organization = self.request.GET.get('organization', None)
        if organization:
            try:
                organization = Organization.objects.get(name=organization)
                organization_users = organization.get_people(self.request.user)
                if organization_users:
                    users = users.filter(pk__in=organization_users.values_list('pk'))
                else:
                    users = []
            except Exception as e:
                raise Exception("Could not find organization" + str(e))

        return {
            'users': users,
            'organizations': organizations
        }
