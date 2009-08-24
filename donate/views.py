from django.shortcuts import render_to_response, get_object_or_404
from wammu_web.wammu.helpers import WammuContext

from wammu_web.donate.forms import DonateForm

from django.utils.translation import ugettext as _

from django.conf import settings

def donate(request):

    # What you want the button to do.
    paypal_dict = {
        'amount': '10.00',
        'item_name': 'Gammu/Wammu donation',
        'currency_code': 'EUR',
        'no_note': '1',
        'page_style': 'Wammu',
    }

    # Create the instance.
    form = DonateForm(initial=paypal_dict, button_type='donate')
    return render_to_response('donate.html', WammuContext(request, {
        'form': form,
    }))

