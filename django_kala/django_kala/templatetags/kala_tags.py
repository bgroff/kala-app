from django.template import Library
from django.utils.translation import ugettext as _


register = Library()


@register.filter
def pretty_user(user):
    if user is None:
        return _('Lost in translation')
    else:
        return '%s %s' % (user.first_name, user.last_name)


@register.filter
def users_projects(organization, user):
    return organization.get_projects(user)


@register.filter(name='split')
def split(value, arg):
    return value.split(arg)


@register.filter(name='header')
def header(value):
    parts = value.split('/')
    if parts[-1] == 'invite_user':
        return 'invite_user'
    if parts[-2] == 'settings':
        return 'settings'
    return 'main'
