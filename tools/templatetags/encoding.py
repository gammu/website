from django import template
from django.template.defaultfilters import stringfilter
from PIL import Image
from StringIO import StringIO

register = template.Library()

@register.filter
@stringfilter
def hex(value):
    return value.encode('hex')

@register.filter
@stringfilter
def base64(value):
    return value.encode('base64')

@register.filter
def xpm2png(value):
    xpm = '''/* XPM */
static char * ala_xpm[] = {
"%s"};''' % '",\n"'.join(value)
    xpm = xpm.replace('None', '#ffffff').replace('Black', '#000000')
    io = StringIO(xpm)
    im = Image.open(io)
    outio = StringIO()
    im.save(outio, 'png')
    # I don't understand why, but this is needed to get data to buf
    outio.read()
    return outio.buf.encode('base64')

@register.filter
@stringfilter
def wrap(value):
    ret = ''
    while len(value) > 0:
        ret += '%s\n' % value[:32]
        value = value[32:]
    return ret
