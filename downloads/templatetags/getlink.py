from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from downloads.models import PLATFORM_CHOICES

register = template.Library()


@register.simple_tag
def getlink(item):
    return ''.join(('https://dl.cihar.com', item.location))


@register.simple_tag
def platform_info(program, platform):

    platform_name = platform
    for c in PLATFORM_CHOICES:
        if platform == c[0]:
            platform_name = c[1]

    ret = ['<h3>{0}</h3>'.format(platform_name)]
    ret.append(
        render_to_string(
            'downloads/programs/{0}-{1}.html'.format(
                program,
                platform
            )
        )
    )
    return mark_safe('\n'.join(ret))
