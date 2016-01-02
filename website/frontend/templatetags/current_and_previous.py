from django import template

register = template.Library()


@register.filter
def current_and_previous(entry_list):
    new_list = []

    for i in range(len(entry_list)):
        current = entry_list[i]
        if i + 1 < len(entry_list):
            previous = entry_list[i + 1]
        else:
            previous = None

        new_list.append((previous, current))

    return new_list
