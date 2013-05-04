from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from kala.views import LoginRequiredMixin
from companies.forms import CreateCompanyForm
from companies.models import Companies
from projects.models import Projects
from .forms import PersonForm, CreatePersonForm, permission_forms, DeletedCompanyForm
from .models import People


class EditProfile(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = {
            'form': self.form,
            'person': self.person,
        }
        if self.request.user.is_admin:
            context['permission_forms'] = self.permission_forms
        return context

    def dispatch(self, request, pk, *args, **kwargs):
        self.person = get_object_or_404(People.active, pk=pk)
        if self.person != request.user and not request.user.is_admin:
            messages.error(request, 'You do not have permission to edit this persons account')
            return redirect(reverse('home'))
        self.form = PersonForm(request.POST or None, instance=self.person)
        if request.user.is_admin:
            self.permission_forms = permission_forms(request, self.person)
        return super(EditProfile, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'toggle-admin' in request.POST and request.user.is_admin:
            self.person.is_admin = not self.person.is_admin
            self.person.save()
            if self.person.is_admin:
                messages.success(request, 'This user has been granted administrator privileges')
            else:
                messages.success(request, 'This user has had it\'s administrator privileges revoked')
            return redirect(reverse('edit_profile', args=[self.person.pk]))

        if 'delete' in request.POST and request.user.is_admin:
            self.person.set_active(False)
            messages.success(request, 'The person has been removed')
            return redirect(reverse('people'))

        if 'save-permissions' in request.POST:
            all_valid = True
            for form in self.permission_forms:
                if form.is_valid():
                    form.save()
                else:
                    all_valid = False
            if all_valid:
                messages.success(request, 'The permissions have been updated')
                return redirect(reverse('edit_profile', args=[self.person.pk]))

        if self.form.is_valid():
            self.form.save()
            messages.success(request, 'Profile data has been saved')
            return redirect(reverse('edit_profile', args=[self.person.pk]))
        return self.render_to_response(self.get_context_data())


class PeopleView(LoginRequiredMixin, TemplateView):
    template_name = 'people.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_admin:
            return {
                'companies': self.companies,
                'company_form': self.company_form,
                'person_form': self.person_form,
                'undelete_form': self.undelete_form,
            }
        return {
            'companies': self.companies
        }

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin:
            self.companies = Companies.active.all()
            self.company_form = CreateCompanyForm(request.POST if 'create_company' in request.POST else None)
            self.person_form = CreatePersonForm(request.POST if 'create_person' in request.POST else None)
            self.undelete_form = DeletedCompanyForm(request.POST if 'undelete' in request.POST else None)
        else:
            self.companies = Companies.active.filter(
                pk__in=Projects.clients.through.objects.filter(people__pk=self.request.user.pk).values(
                    'projects__company__pk'))
            self.companies = self.companies | Companies.active.filter(pk=self.request.user.company.pk)
        return super(PeopleView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'You do not have permission to create data')
            return redirect(reverse('people'))
        #raise Exception(str(request.POST))
        if 'create_company' in request.POST and self.company_form.is_valid():
            company = self.company_form.save()
            messages.success(request, 'The company has been created')
            return redirect(reverse('company', args=[company.pk]))
        if 'create_person' in request.POST and self.person_form.is_valid():
            self.person_form.save()
            messages.success(request, 'The person has been created')
            return redirect(reverse('people'))
        if 'undelete' in request.POST and self.undelete_form.is_valid():
            company = self.undelete_form.save()
            messages.success(request, 'The company %s has been un-deleted' % company.name)
            return redirect(reverse('people'))
        return self.render_to_response(self.get_context_data())

