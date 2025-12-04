from django.template import Library
from django.utils.translation import gettext as _


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


@register.filter(name='can_create')
def can_create(obj, user):
    return obj.can_create(user)


@register.filter(name='can_invite')
def can_invite(obj, user):
    return obj.can_invite(user)


@register.filter(name='can_manage')
def can_manage(obj, user):
    return obj.can_manage(user)


@register.simple_tag
def smart_page_range(page_range, current_page, window=2):
    """
    Generate a smart pagination range with ellipsis for large page counts.

    Returns a list of page numbers and None values (representing ellipsis).
    Example: [1, None, 13, 14, 15, 16, 17, None, 30]

    Args:
        page_range: Django paginator's page_range
        current_page: Current page number (can be string or int)
        window: Number of pages to show on each side of current page
    """
    pages = list(page_range)
    if not pages:
        return []

    total_pages = len(pages)
    current = int(current_page)

    # If few enough pages, show all
    if total_pages <= (2 * window + 5):
        return pages

    result = []
    first_page = pages[0]
    last_page = pages[-1]

    # Always include first page
    result.append(first_page)

    # Calculate the window around current page
    window_start = max(current - window, first_page + 1)
    window_end = min(current + window, last_page - 1)

    # Add ellipsis after first page if needed
    if window_start > first_page + 1:
        result.append(None)
    elif window_start == first_page + 1:
        # No gap, just continue
        pass

    # Add pages in the window
    for page in range(window_start, window_end + 1):
        if page not in result:
            result.append(page)

    # Add ellipsis before last page if needed
    if window_end < last_page - 1:
        result.append(None)

    # Always include last page
    if last_page not in result:
        result.append(last_page)

    return result
