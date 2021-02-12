import binascii

import gammu
from django.shortcuts import render

from tools.forms import PDUDecodeForm, PDUEncodeForm


def pduencode(request):
    pdu = None
    if request.method == "POST":
        form = PDUEncodeForm(request.POST)
        if form.is_valid():
            # Prepare message data
            smsinfo = {
                "Class": form.cleaned_data["cls"],
                "Unicode": form.cleaned_data["unicode"],
                "Entries": [
                    {
                        "ID": "ConcatenatedTextLong",
                        "Buffer": form.cleaned_data["text"],
                    }
                ],
            }
            # Encode SMS
            encoded = gammu.EncodeSMS(smsinfo)
            # Fill in remaining data
            for msg in encoded:
                msg["SMSC"] = {
                    "Location": 0,
                    "Number": form.cleaned_data["smsc"],
                    "Validity": "Max",
                }
                msg["Number"] = form.cleaned_data["number"]
                msg["Class"] = form.cleaned_data["cls"]
            # Encode PDU
            pdu = enumerate(gammu.EncodePDU(e, "Submit").hex() for e in encoded)

    else:
        form = PDUEncodeForm()
    return render(
        request,
        "tools/pduencode.html",
        {
            "form": form,
            "pdu": pdu,
        },
    )


def pdudecode(request):
    decoded = None
    smsinfo = None
    if request.method == "POST":
        form = PDUDecodeForm(request.POST)
        if form.is_valid():
            # Decode PDU
            decoded = []
            parts = []
            for i, part in enumerate(form.cleaned_data["text"].split()):
                try:
                    d = gammu.DecodePDU(binascii.unhexlify(part))
                    parts.append([d])
                    if isinstance(d["Text"], bytes):
                        d["TextHex"] = d["Text"].hex()
                    else:
                        d["TextHex"] = None
                    d["UDH"]["TextHex"] = d["UDH"]["Text"].hex()
                    d["Id"] = i + 1
                    d["PDU"] = part
                    decoded.append(d)
                except gammu.GSMError as e:
                    decoded.append({"Error": e.args[0]})
                except Exception as e:
                    decoded.append({"Error": {"Text": str(e)}})
            # Link multipart messages
            linked = gammu.LinkSMS(parts)
            # Decode multipart messages
            smsinfo = []
            part = 1
            for x in linked:
                try:
                    d = gammu.DecodeSMS(x)
                    if d is not None:
                        d["Id"] = part
                        part = part + 1
                        smsinfo.append(d)
                except UnicodeDecodeError as err:
                    smsinfo.append({"Error": str(err), "Id": part, "Unknown": True})
                    part = part + 1

    else:
        form = PDUDecodeForm()
    return render(
        request,
        "tools/pdudecode.html",
        {
            "form": form,
            "decoded": decoded,
            "smsinfo": smsinfo,
        },
    )


def countries(request):
    countries = gammu.GSMCountries.items()
    return render(
        request,
        "tools/countries.html",
        {
            "countries": sorted(countries),
        },
    )


def networks(request):
    if "country" in request.GET:
        country = request.GET["country"]
        networks = [x for x in gammu.GSMNetworks.items() if x[0].startswith(country)]
    else:
        networks = gammu.GSMNetworks.items()
    return render(
        request,
        "tools/networks.html",
        {
            "networks": sorted(networks),
        },
    )
