from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
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
    query = request.GET.get('q', None)
    features = request.GET.getlist('feature')

    phones = Phone.objects.exclude(state = 'deleted')
    urlparams = []

    # Filter for features
    if len(features) > 0:
        phones = phones.filter(connection__isnull = False)
        for feature in features:
            urlparams.append('feature=%s' % feature)
            phones = phones.filter(features__name = feature)

    # Filter for query string
    if query is not None:
        urlparams.append('q=%s' % query)
        query = query.strip()
        for part in query.split():
            phones = phones.filter(
                Q(vendor__name__icontains = part) |
                Q(name__icontains = part))

    # Sort results
    phones = phones.order_by('vendor__name', 'name')

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

    return render_to_response('phonedb/search.html', WammuContext(request, {
        'phones': phones,
        'urlparams': '&'.join(urlparams),
    }))

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
