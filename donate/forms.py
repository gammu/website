from paypal.standard.conf import (POSTBACK_ENDPOINT, SANDBOX_POSTBACK_ENDPOINT,
    RECEIVER_EMAIL)
from paypal.standard.forms import PayPalPaymentsForm
from django import forms

from django.utils.translation import ugettext as _

from django.utils.safestring import mark_safe

class DonateForm(PayPalPaymentsForm):
    def __init__(self, *args, **kwargs):
        super(DonateForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget = forms.TextInput()
        self.fields['amount'].label = _('Amount (EUR)')
        self.fields['custom'].widget = forms.TextInput()
        self.fields['custom'].label = _('Message from you')
        self.cmd = '_donations'

    def render(self):
        return mark_safe(u"""<form action="%s" method="post">
        <table>
    %s
    <tr><th colspan="2">
    <input type="submit" value="%s" name="submit" />
    </th></tr>
    </table>
</form>""" % (POSTBACK_ENDPOINT, self.as_table(), _("Donate")))


    def sandbox(self):
        return mark_safe(u"""<form action="%s" method="post">
        <table>
    %s
    <tr><th colspan="2">
    <input type="submit" value="%s" name="submit" />
    </th></tr>
    </table>
</form>""" % (SANDBOX_POSTBACK_ENDPOINT, self.as_table(), _("Donate")))

