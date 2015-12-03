from django import template

register = template.Library()


@register.filter
def current_and_previous(entry_list):

    new_list = []
    last_entry = None

    for entry in entry_list:
        new_list.append((last_entry, entry))

        last_entry = entry

    return new_list
