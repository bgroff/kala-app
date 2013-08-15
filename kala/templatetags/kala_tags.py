from django.utils.functional import SimpleLazyObject
from django.template import Library
from types import NoneType
from accounts.models import Person
from companies.models import Companies

register = Library()


@register.filter
def pretty_user(user):
    assert type(
        user) is Person or NoneType or SimpleLazyObject, 'The user must either be of type People or None, got %s' % type(
        user)
    if user is None:
        return 'Lost in translation'
    else:
        return '%s %s' % (user.first_name, user.last_name)


@register.filter
def users_projects(company, user):
    assert type(company) is Companies, 'The company must be of type Company, got %s' % type(company)
    assert type(
        user) is Person or NoneType or SimpleLazyObject, 'The user must either be of type People or None, got %s' % type(
        user)
    return company.get_project_list(user)

