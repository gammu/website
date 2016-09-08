from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from downloads.models import Mirror, PLATFORM_CHOICES

register = template.Library()


@register.simple_tag
def getlink(dlname):
    mirror = Mirror.objects.get(slug='cihar-com')
    return mirror.getlink(dlname)


@register.simple_tag
def platform_info(program, platform):

    platform_name = platform
    for c in PLATFORM_CHOICES:
        if platform == c[0]:
            platform_name = c[1]

    ret = ['<h4>{0}</h4>'.format(platform_name)]
    ret.append(
        render_to_string(
            'downloads/programs/{0}-{1}.html'.format(
                program,
                platform
            )
        )
    )
    return mark_safe('\n'.join(ret))
