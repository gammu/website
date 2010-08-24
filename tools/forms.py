from django.forms import Form
from django import forms
from django.utils.translation import ugettext_lazy

class PDUDecodeForm(Form):
    text = forms.RegexField(
        label = ugettext_lazy('PDU text'),
        regex = '^([a-fA-F0-9]{2})+([\r\n]+([a-fA-F0-9]{2})+)*$',
        widget = forms.Textarea,
        help_text = ugettext_lazy('You can provide more messages, each on seaprate line.'))

class PDUEncodeForm(Form):
    text = forms.CharField(label = ugettext_lazy('Text'))
    cls = forms.ChoiceField(label = ugettext_lazy('Class'), choices = [(0, '0 - Standard'), (1, '1 - Flash')])
    unicode = forms.BooleanField(label = ugettext_lazy('Unicode'), required = False)
    number = forms.CharField(label = ugettext_lazy('Recipient'))
    smsc = forms.CharField(label = ugettext_lazy('SMSC number'))
