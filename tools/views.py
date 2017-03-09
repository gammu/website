from forms import PDUDecodeForm, PDUEncodeForm
from django.shortcuts import render
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
    return render(request, 'tools/pduencode.html', {
        'form': form,
        'pdu': pdu,
    })

def pdudecode(request):
    decoded = None
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
                except gammu.GSMError as e:
                    decoded.append({'Error': e[0]})
                except Exception as e:
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
    return render(request, 'tools/pdudecode.html', {
        'form': form,
        'decoded': decoded,
        'smsinfo': smsinfo,
    })

def countries(request):
    countries = gammu.GSMCountries.items()
    countries.sort()
    return render(request, 'tools/countries.html', {
        'countries': countries,
    })

def networks(request):
    if 'country' in request.GET:
        country = request.GET['country']
        l = len(country)
        networks = [x for x in gammu.GSMNetworks.items() if x[0][:l] == country]
    else:
        networks = gammu.GSMNetworks.items()
    networks.sort()
    return render(request, 'tools/networks.html', {
        'networks': networks,
    })
