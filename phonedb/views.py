from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.db.models import Q
from django.template import RequestContext
from phonedb.models import Vendor, Phone, Feature, Connection, GARBLE_CHOICES
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.utils.translation import ugettext as _
import csv
import socket
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.contrib.sites.models import Site

import datetime
from pygooglechart import SimpleLineChart
from pygooglechart import Axis
from pygooglechart import Chart

from phonedb.forms import SearchForm, NewForm

# Create your views here.

def get_chart_url():
    cache_key = 'phonedb-chart-url-%s' % settings.LANGUAGE_CODE
    url = cache.get(cache_key)
    if url is not None:
        return url
    enddate = datetime.datetime.now()
    # This works badly, we will rather render only chart for month after
    # it has finished
    #+ datetime.timedelta(days=30)
    endyear = enddate.year
    endmonthlast = enddate.month
    endmonth = 12

    dates = []
    unsupported = []
    supported = []
    totals = []
    alls = []
    years = []

    for year in xrange(2006, endyear + 1):
        if year == endyear:
            endmonth = endmonthlast
        for month in xrange(1, endmonth + 1):
            if month == 1:
                years.append('%d' % year)
            else:
                years.append('')

            time_range = (datetime.date(1900, 1, 1), datetime.date(year, month, 1))

            supported_val = Phone.objects.exclude(state = 'deleted').filter(connection__isnull = False).filter(created__range = time_range).count()
            unsupported_val = Phone.objects.exclude(state = 'deleted').filter(connection__isnull = True).filter(created__range = time_range).count()
            all_val = Phone.objects.filter(created__lt = datetime.date(year, month, 1)).count()

            supported.append(supported_val)
            unsupported.append(unsupported_val)
            totals.append(unsupported_val + supported_val)
            alls.append(all_val)
            dates.append('%d-%02d' % (year, month))

#print dates
#print unsupported
#print supported
#print totals
#print alls

    max_y = ((max(alls) / 100) + 1) * 100

    chart = SimpleLineChart(800, 300, y_range=[0, max_y])


#    chart.fill_solid(chart.BACKGROUND, 'ffd480')
#    chart.fill_solid(chart.CHART, 'ffd480')
# Chart data
    chart.add_data(supported)
    chart.add_data(totals)
    chart.add_data(alls)
# Lowest value
    chart.add_data([0] * 2)

# Set the line colour to blue
    chart.set_colours(['00FF00', 'FF0000', '0000FF', '00000000'])

#chart.add_fill_range('76A4FB', 2, 3)
# Set the vertical stripes
    month_stripes = 3.0
    chart.fill_linear_stripes(Chart.CHART, 0, 'ffffff', month_stripes / len(alls), 'cccccc', month_stripes / len(alls))

# Set the horizontal dotted lines
    chart.set_grid(0, 10, 5, 5)

    chart.set_legend([
        _('Supported phones').encode('utf-8'),
        _('Approved records').encode('utf-8'),
        _('Total records').encode('utf-8')])

    left_axis = map(lambda x: '%d' % x, xrange(0, max_y + 1, max_y / 10))
    left_axis[0] = ''
    chart.set_axis_labels(Axis.LEFT, left_axis)

    chart.set_axis_labels(Axis.BOTTOM, years)

    url = chart.get_url().replace('http:', 'https:')
    cache.set(cache_key, url, 3600)
    return url


def phones_chart(request):
    return HttpResponseRedirect(get_chart_url())

def get_feeds():
    return [
        {'url': '/phones/rss/', 'title': _('Gammu Phone Database Feed (RSS)'), 'type': 'application/rss+xml'},
        {'url': '/phones/atom/', 'title': _('Gammu Phone Database Feed (Atom)'), 'type': 'application/atom+xml'},
        ]


def index(request):
    vendors = Vendor.objects.all().order_by('name')
    phones = Phone.objects.filter(state__in = ['approved', 'draft']).order_by('-created')[:settings.PHONES_ON_INDEX]
    return render_to_response('phonedb/index.html', RequestContext(request, {
        'vendors': vendors,
        'phones': phones,
        'features': Feature.objects.all().order_by('name'),
        'chart_url': get_chart_url(),
        'feeds': get_feeds(),
        'form': SearchForm(),
    }))

def search(request, featurename = None):
    # We need a copy, because we might want to add a feature from URL
    rq = request.GET.copy()
    if featurename is not None:
        rq.appendlist('feature', featurename)
    form = SearchForm(rq)
    if form.is_valid():
        query = form.cleaned_data['q']
        features = list(set(form.cleaned_data['feature']))

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
    else:
        phones = Phone.objects.all()
        urlparams = []

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

    return render_to_response('phonedb/search.html', RequestContext(request, {
        'phones': phones,
        'urlparams': '&'.join(urlparams),
        'feeds': get_feeds(),
        'form': form,
    }))

@login_required
def review(request):
    phones = Phone.objects.filter(state = 'draft')

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

    return render_to_response('phonedb/search.html', RequestContext(request, {
        'phones': phones,
        'feeds': get_feeds(),
    }))

def vendor(request, vendorname):
    vendor = get_object_or_404(Vendor, slug = vendorname)
    phones = Phone.objects.filter(vendor = vendor, state__in=('approved', 'draft')).order_by('name')

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

    return render_to_response('phonedb/vendor.html', RequestContext(request, {
        'vendor': vendor,
        'phones': phones,
        'feeds': get_feeds(),
    }))

def phone_redirect(request):
    try:
        id = int(request.GET['id'])
    except:
        raise Http404('No such page!')
    phone = get_object_or_404(Phone, id = id)
    return HttpResponseRedirect(phone.get_absolute_url())

def phone(request, vendorname, id):
    id = int(id)
    vendor = get_object_or_404(Vendor, slug = vendorname)
    phone = get_object_or_404(Phone, id = id, vendor = vendor)
    related = Phone.objects.filter(vendor = vendor, name__icontains = phone.name).exclude(id = id).exclude(state = 'deleted')
    return render_to_response('phonedb/phone.html', RequestContext(request, {
        'vendor': vendor,
        'phone': phone,
        'related': related,
        'feeds': get_feeds(),
        'user': request.user,
    }))

@login_required
def approve(request, vendorname, id):
    id = int(id)
    vendor = get_object_or_404(Vendor, slug = vendorname)
    phone = get_object_or_404(Phone, id = id, vendor = vendor)

    if not request.user.is_superuser:
        return HttpResponseRedirect(phone.get_absolute_url())

    phone.state = 'approved'
    phone.save()
    return HttpResponseRedirect('/phones/review/')

@login_required
def delete(request, vendorname, id):
    id = int(id)
    vendor = get_object_or_404(Vendor, slug = vendorname)
    phone = get_object_or_404(Phone, id = id, vendor = vendor)

    if not request.user.is_superuser:
        return HttpResponseRedirect(phone.get_absolute_url())

    phone.state = 'deleted'
    phone.save()
    return HttpResponseRedirect('/phones/review/')

def phones_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=gammu-phones.csv'

    writer = csv.writer(response)
    phones = Phone.objects.filter(state__in = ['approved', 'draft']).order_by('id')
    writer.writerow(['Link','Manufacturer','Name','Author','Date','Connection','Features','Gammu-Version'])
    try:
        current_site = Site.objects.get_current(request)
    except Site.DoesNotExist:
        current_site = 'wammu.eu'
    for phone in phones:
        if phone.connection is None:
            conn = ''
        else:
            conn = phone.connection.name
        author = phone.get_author(html = False)
        if author is None:
            author = ''
        writer.writerow([
            'https://%s%s' % (current_site, phone.get_absolute_url()),
            phone.vendor.name.encode('utf8'),
            phone.name.encode('utf8'),
            author.encode('utf8'),
            phone.created.isoformat().encode('utf8'),
            conn.encode('utf8'),
            u','.join([f.name for f in phone.features.all()]).encode('utf8'),
            phone.gammu_version.encode('utf8')
            ])


    return response

@csrf_exempt
def create_wammu(request):
    '''
    Compatibility interface for Wammu.
    '''
    INVALID = 'Invalid values: %s'
    OKAY = 'Entry created, id=%d, url=/gammu/phonedb/%s/%d'
    OKAY_V2 = 'Entry created, id=%d, url=%s'
    invalid = []
    version = 1
    response = HttpResponse(content_type='text/plain')

    if not request.POST.has_key('irobot') or request.POST['irobot'] != 'wammu':
        invalid.append('irobot')

    if request.POST.has_key('version'):
        version = int(request.POST['version'])

    phone = Phone()

    try:
        phone.vendor = Vendor.objects.get(pk = int(request.POST['manufacturer']))
    except:
        invalid.append('vendor')

    try:
        phone.name = request.POST['name']
        if len(phone.name) == 0:
            invalid.append('name')
    except:
        invalid.append('name')

    try:
        phone.connection = Connection.objects.get(name = request.POST['connection'])
    except:
        invalid.append('connection')

    try:
        phone.model = request.POST['model']
        if phone.model == 'auto':
            phone.model = ''
    except:
        invalid.append('model')

    try:
        phone.note = request.POST['note']
    except:
        invalid.append('note')

    try:
        phone.author_name = request.POST['author_name']
    except:
        invalid.append('author_name')

    try:
        phone.author_email = request.POST['author_email']
    except:
        invalid.append('author_email')

    try:
        phone.email_garble = request.POST['email_garble']
        if not phone.email_garble in [x[0] for x in GARBLE_CHOICES]:
            invalid.append('email_garble')
    except:
        invalid.append('email_garble')

    try:
        phone.gammu_version = request.POST['gammu_version']
    except:
        invalid.append('gammu_version')

    try:
        phone.full_clean()
    except ValidationError, e:
        invalid.extend(e.message_dict.keys())
        invalid = list(set(invalid))

    if len(invalid) > 0:
        response.write(INVALID % ','.join(invalid))
        return response

    features = []
    for feature in Feature.objects.all():
        key = 'fts[%s]' % feature.name
        if request.POST.has_key(key) and request.POST[key] == '1':
            features.append(feature)

    phone.save()

    for feature in features:
        phone.features.add(feature)

    if version == 2:
        response.write(OKAY_V2 % (phone.id, phone.get_absolute_url()))
    else:
        response.write(OKAY % (phone.id, phone.vendor.slug, phone.id))
    return response

def create(request, vendorname = None):
    # Check if we did not receive legacy request
    if request.method == 'POST' and request.POST.has_key('irobot') and request.POST['irobot'] == 'wammu':
        return create_wammu(request)

    if request.method == 'POST' and request.POST.has_key('irobot') and request.POST['irobot'] == 'nospam':
        form = NewForm(request.POST)
        if form.is_valid():
            newphone = form.save()
            newphone.address = request.META.get('REMOTE_ADDR')
            if newphone.address[:7] == '::ffff:':
                newphone.address = newphone.address[7:]
            try:
                newphone.hostname = socket.gethostbyaddr(newphone.address)[0]
            except socket.herror:
                newphone.hostname = newphone.address
            newphone.save()
            result = HttpResponseRedirect(newphone.get_absolute_url())
            request.session['message'] = _('Phone record has been created.')
            result.set_cookie('phonedb_garble', form.cleaned_data['email_garble'].encode('utf-8'), max_age = 3600 * 24 * 365)
            result.set_cookie('phonedb_author', form.cleaned_data['author_name'].encode('utf-8'), max_age = 3600 * 24 * 365)
            result.set_cookie('phonedb_email', form.cleaned_data['author_email'].encode('utf-8'), max_age = 3600 * 24 * 365)
            return result
    else:
        initial = {}
        try:
            if vendorname is not None:
                vendor = Vendor.objects.get(slug = vendorname)
            else:
                vendor = Vendor.objects.get(slug = request.GET['vendor'])
            initial['vendor'] = vendor.id
        except:
            pass
        try:
            initial['name'] = request.GET['name']
        except:
            pass
        try:
            initial['email_garble'] = request.COOKIES['phonedb_garble']
        except:
            pass
        try:
            initial['author_name'] = request.COOKIES['phonedb_author']
        except:
            pass
        try:
            initial['author_email'] = request.COOKIES['phonedb_email']
        except:
            pass

        form = NewForm(initial = initial)

    return render_to_response('phonedb/new.html', RequestContext(request, {
        'form': form,
        'feeds': get_feeds(),
    }))
