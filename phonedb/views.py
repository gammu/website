from django.shortcuts import render_to_response, get_object_or_404
from wammu_web.wammu.helpers import WammuContext
from wammu_web.phonedb.models import Vendor, Phone, Feature
from django.core.paginator import Paginator, InvalidPage, EmptyPage

# Create your views here.

def index(request):
    return

def search(request):
    return

def feature(request, featurename):
    return

def vendor(request, vendorname):
    return

def phone(request, vendorname, id):
    vendor = get_object_or_404(Vendor, slug = vendorname)
    phone = get_object_or_404(Phone, id = int(id), vendor = vendor)
    return render_to_response('phonedb/phone.html', WammuContext(request, {
        'vendor': vendor,
        'phone': phone,
    }))
