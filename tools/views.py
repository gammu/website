# Create your views here.
from forms import PDUDecodeForm, PDUEncodeForm
from django.shortcuts import render_to_response
from django.template import RequestContext
import gammu

def pduencode(request):
    pdu = None
    if request.method == 'POST':
        form = PDUEncodeForm(request.POST)
        if form.is_valid():
            # Prepare message data
            smsinfo = {
                'Class': form.cleaned_data['cls'],
                'Unicode': form.cleaned_data['unicode'],
                'Entries':  [
                    {
                        'ID': 'ConcatenatedTextLong',
                        'Buffer': form.cleaned_data['text'],
                    }
                ]}
            # Encode SMS
            encoded = gammu.EncodeSMS(smsinfo)
            # Fill in remaining data
            for msg in encoded:
                msg['SMSC'] = {
                        'Location': 0,
                        'Number': form.cleaned_data['smsc'],
                        'Validity': 'Max',
                        }
                msg['Number'] = form.cleaned_data['number']
                msg['Class'] = form.cleaned_data['cls']
            # Encode PDU
            pdu = enumerate([gammu.EncodePDU(e, 'Submit').encode('hex') for e in encoded])

    else:
        form = PDUEncodeForm()
    return render_to_response('tools/pduencode.html', RequestContext(request, {
        'form': form,
        'pdu': pdu,
    }))

def pdudecode(request):
    decoded = None
    error = None
    smsinfo = None
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
                    if type(d['Text']) == unicode:
                        d['TextHex'] = None
                    else:
                        d['TextHex'] = d['Text'].encode('hex')
                    d['UDH']['TextHex'] = d['UDH']['Text'].encode('hex')
                    d['Id'] = i + 1
                    d['PDU'] = part
                    decoded.append(d)
                except gammu.GSMError, e:
                    decoded.append({'Error': e[0]})
                except Exception, e:
                    decoded.append({'Error': {'Text': str(e)}})
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
