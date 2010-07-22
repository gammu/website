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
            decoded = []
            for i, part in enumerate(form.cleaned_data['text'].split()):
                try:
                    d = gammu.DecodePDU(part.decode('hex'))
                    d['TextHex'] = d['Text'].encode('hex')
                    d['UDH']['TextHex'] = d['UDH']['Text'].encode('hex')
                    decoded.append(d)
                except gammu.GSMError, e:
                    decoded.append({'Error': e[0]})
                d['Id'] = i + 1
                d['PDU'] = part
    else:
        form = PDUDecodeForm()
    return render_to_response('tools/pdudecode.html', RequestContext(request, {
        'form': form,
        'decoded': decoded,
    }))
