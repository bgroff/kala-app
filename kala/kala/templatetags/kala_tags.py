from django.utils.functional import SimpleLazyObject
from django.template import Library
from accounts.models import Person
from companies.models import Company

register = Library()


@register.filter
def pretty_user(user):
    if user is None:
        return 'Lost in translation'
    else:
        return '%s %s' % (user.first_name, user.last_name)


@register.filter
def users_projects(company, user):
    return company.get_project_list(user)

