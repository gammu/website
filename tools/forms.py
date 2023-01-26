from django import forms
from django.forms import Form
from django.utils.translation import gettext_lazy


class PDUDecodeForm(Form):
    text = forms.RegexField(
        label=gettext_lazy("PDU text"),
        regex="^([a-fA-F0-9]{2})+([\r\n]+([a-fA-F0-9]{2})+)*$",
        widget=forms.Textarea,
        help_text=gettext_lazy("You can provide more messages, each on separate line."),
    )


class PDUEncodeForm(Form):
    text = forms.CharField(label=gettext_lazy("Text"))
    cls = forms.ChoiceField(
        label=gettext_lazy("Class"), choices=[(0, "0 - Standard"), (1, "1 - Flash")]
    )
    unicode = forms.BooleanField(label=gettext_lazy("Unicode"), required=False)
    number = forms.CharField(label=gettext_lazy("Recipient"))
    smsc = forms.CharField(label=gettext_lazy("SMSC number"))
