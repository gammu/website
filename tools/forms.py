from django.forms import Form
from django import forms

class PDUDecodeForm(Form):
    text = forms.RegexField(label = 'PDU text', regex = '^([a-fA-F0-9]{2})+$')

