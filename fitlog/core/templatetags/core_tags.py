from django import template
from django.contrib import messages

register = template.Library()


@register.filter()
def alert_type(value):
    tag = messages.DEFAULT_TAGS.get(value, 'info')
    if tag == 'error':
        return 'danger'
    elif value == 'debug':
        return 'secondary'
    return tag
