from django import template

register = template.Library()

class GetLink(template.Node):
    def __init__(self, dlname):
        self.dlname = template.Variable(dlname)
        self.mirror =  template.Variable('mirror')

    def render(self, context):
        mirror = self.mirror.resolve(context)
        download = self.dlname.resolve(context)
        return mirror.getlink(download)

@register.tag
def getlink(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, dlname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % token.split_contents()[0]

    return GetLink(dlname)
