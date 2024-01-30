from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from downloads.models import PLATFORM_CHOICES

register = template.Library()


@register.simple_tag
def getlink(item):
    return f"https://dl.cihar.com{item.location}"


@register.simple_tag
def platform_info(program, platform):
    platform_name = platform
    for c in PLATFORM_CHOICES:
        if platform == c[0]:
            platform_name = c[1]

    ret = [f"<h3>{platform_name}</h3>"]
    ret.append(render_to_string(f"downloads/programs/{program}-{platform}.html"))
    return mark_safe("\n".join(ret))
