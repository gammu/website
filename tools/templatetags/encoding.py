from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def hex(value):
    return value.encode('hex')

@register.filter
@stringfilter
def wrap(value):
    ret = ''
    while len(value) > 0:
        ret += '%s\n' % value[:32]
        value = value[32:]
    return ret
