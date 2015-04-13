from django import template
from downloads.models import Mirror

register = template.Library()


@register.simple_tag
def getlink(dlname):
    mirror = Mirror.objects.get(slug='cihar-com')
    return mirror.getlink(dlname)
