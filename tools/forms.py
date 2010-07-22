from django.forms import Form
from django import forms
from django.utils.translation import ugettext_lazy

class PDUDecodeForm(Form):
    text = forms.RegexField(
        label = ugettext_lazy('PDU text'),
        regex = '^([a-fA-F0-9]{2})+([\r\n]+([a-fA-F0-9]{2})+)*$',
        widget = forms.Textarea,
        help_text = ugettext_lazy('You can provide more messages, each on seaprate line.'))

