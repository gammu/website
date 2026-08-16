from django import forms
from django.forms import Form
from django.utils.translation import gettext_lazy


class PDUDecodeForm(Form):
    text = forms.RegexField(
        label=gettext_lazy("PDU text"),
        regex="^([a-fA-F0-9]{2})+([\r\n]+([a-fA-F0-9]{2})+)*$",
        widget=forms.Textarea,
        max_length=5000,
        help_text=gettext_lazy("You can provide more messages, each on separate line."),
    )

    def clean_text(self):
        value = self.cleaned_data["text"]
        messages = value.split()
        if len(messages) > 50:
            raise forms.ValidationError(
                gettext_lazy("You can provide at most 50 PDU messages.")
            )
        if any(len(message) > 512 for message in messages):
            raise forms.ValidationError(
                gettext_lazy("Each PDU can contain at most 512 hexadecimal characters.")
            )
        return value


class PDUEncodeForm(Form):
    text = forms.CharField(label=gettext_lazy("Text"), max_length=1000)
    cls = forms.ChoiceField(
        label=gettext_lazy("Class"),
        choices=[(0, "0 - Standard"), (1, "1 - Flash")],
    )
    unicode = forms.BooleanField(label=gettext_lazy("Unicode"), required=False)
    number = forms.CharField(label=gettext_lazy("Recipient"))
    smsc = forms.CharField(label=gettext_lazy("SMSC number"))
