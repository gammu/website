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
            # Decode PDU
            decoded = []
            parts = []
            for i, part in enumerate(form.cleaned_data['text'].split()):
                try:
                    d = gammu.DecodePDU(part.decode('hex'))
                    parts.append([d])
                    d['TextHex'] = d['Text'].encode('hex')
                    d['UDH']['TextHex'] = d['UDH']['Text'].encode('hex')
                    d['Id'] = i + 1
                    d['PDU'] = part
                    decoded.append(d)
                except gammu.GSMError, e:
                    decoded.append({'Error': e[0]})
            # Link multipart messages
            linked = gammu.LinkSMS(parts)
            # Decode multipart messages
            smsinfo = []
            part = 1
            for x in linked:
                d = gammu.DecodeSMS(x)
                if d is not None:
                    d['Id'] = part
                    part = part + 1
                    smsinfo.append(d)

    else:
        form = PDUDecodeForm()
    return render_to_response('tools/pdudecode.html', RequestContext(request, {
        'form': form,
        'decoded': decoded,
        'smsinfo': smsinfo,
    }))
