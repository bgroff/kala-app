from django.template import Library


register = Library()


@register.filter
def pretty_user(user):
    if user is None:
        return 'Lost in translation'
    else:
        return '%s %s' % (user.first_name, user.last_name)


@register.filter
def users_projects(organization, user):
    return organization.get_projects(user)
