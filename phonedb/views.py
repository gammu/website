from django.shortcuts import render_to_response, get_object_or_404
from wammu_web.wammu.helpers import WammuContext
from wammu_web.phonedb.models import Vendor, Phone, Feature
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.conf import settings

# Create your views here.

def index(request):
    vendors = Vendor.objects.all().order_by('name')
    phones = Phone.objects.filter(state__in = ['approved', 'draft']).order_by('-created')[:settings.PHONES_ON_INDEX]
    return render_to_response('phonedb/index.html', WammuContext(request, {
        'vendors': vendors,
        'phones': phones,
        'features': Feature.objects.all().order_by('name'),
    }))

def search(request):
    return

def feature(request, featurename):
    return

def vendor(request, vendorname):
    vendor = get_object_or_404(Vendor, slug = vendorname)
    phones = Phone.objects.filter(vendor = vendor, state = 'approved').order_by('name')

    paginator = Paginator(phones, settings.PHONES_PER_PAGE, orphans = 5)
    try:
        page = int(request.GET.get('page', '1'))
        if page < 1:
            page = 0
        elif page > paginator.num_pages:
            page = paginator.num_pages
    except ValueError:
        page = 1

    try:
        phones = paginator.page(page)
    except (EmptyPage, InvalidPage):
        phones = paginator.page(1)

    return render_to_response('phonedb/vendor.html', WammuContext(request, {
        'vendor': vendor,
        'phones': phones,
    }))

def phone(request, vendorname, id):
    id = int(id)
    vendor = get_object_or_404(Vendor, slug = vendorname)
    phone = get_object_or_404(Phone, id = id, vendor = vendor)
    related = Phone.objects.filter(vendor = vendor, name__icontains = phone.name, state = 'approved').exclude(id = id)
    return render_to_response('phonedb/phone.html', WammuContext(request, {
        'vendor': vendor,
        'phone': phone,
        'related': related,
    }))
