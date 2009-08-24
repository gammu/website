from django.shortcuts import render_to_response, get_object_or_404
from wammu_web.wammu.helpers import WammuContext

from paypal.standard.forms import PayPalPaymentsForm

from django import forms

from django.conf import settings


def donate(request):

    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "10.00",
        "item_name": "Gammu/Wammu donation",
        'currency_code': 'EUR',
        'cmd': '_donations',
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict, button_type='donate')
#    form.amount.widget = forms.TextInput()
    return render_to_response('donate.html', WammuContext(request, {
        'form': form,
    }))

