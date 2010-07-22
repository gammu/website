# Create your views here.
from forms import PDUDecodeForm
from django.shortcuts import render_to_response
from django.template import RequestContext
import gammu

def pduencode(request):
    return None

def pdudecode(request):
    decoded = None
    error = None
    if request.method == 'POST':
        form = PDUDecodeForm(request.POST)
        if form.is_valid():
            try:
                decoded = gammu.DecodePDU(form.cleaned_data['text'].decode('hex'))
            except gammu.GSMError, e:
                error = e[0]
    else:
        form = PDUDecodeForm()
    return render_to_response('tools/pdudecode.html', RequestContext(request, {
        'form': form,
        'decoded': decoded,
        'error': error,
        'decoded2': repr(decoded),
    }))
