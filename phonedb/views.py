import csv
import datetime
import socket

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.db.models import Count, Q
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from pygooglechart import Axis, Chart, SimpleLineChart

from phonedb.forms import NewForm, SearchForm
from phonedb.models import GARBLE_CHOICES, Connection, Feature, Phone, Vendor

# API responses, need to stay for Wammu compatibility
INVALID = "Invalid values: %s"
OKAY = "Entry created, id=%d, url=/gammu/phonedb/%s/%d"
OKAY_V2 = "Entry created, id=%d, url=%s"


def get_chart_url(force=False):
    cache_key = "phonedb-chart-url-%s" % settings.LANGUAGE_CODE
    url = cache.get(cache_key)
    if url is not None and not force:
        return url
    enddate = timezone.now()
    endyear = enddate.year
    endmonthlast = enddate.month
    endmonth = 12

    dates = []
    unsupported = []
    supported = []
    totals = []
    alls = []
    years = []

    for year in range(2006, endyear + 1):
        if year == endyear:
            endmonth = endmonthlast
        for month in range(1, endmonth + 1):
            if month == 1:
                years.append("%d" % year)
            else:
                years.append("")

            time_range = (
                datetime.datetime(1900, 1, 1, tzinfo=datetime.timezone.utc),
                datetime.datetime(year, month, 1, tzinfo=datetime.timezone.utc),
            )

            supported_val = (
                Phone.objects.exclude(state="deleted")
                .filter(connection__isnull=False)
                .filter(created__range=time_range)
                .count()
            )
            unsupported_val = (
                Phone.objects.exclude(state="deleted")
                .filter(connection__isnull=True)
                .filter(created__range=time_range)
                .count()
            )
            all_val = Phone.objects.filter(
                created__lt=datetime.date(year, month, 1)
            ).count()

            supported.append(supported_val)
            unsupported.append(unsupported_val)
            totals.append(unsupported_val + supported_val)
            alls.append(all_val)
            dates.append("%d-%02d" % (year, month))

    max_y = int(((max(alls) / 100) + 1) * 100)

    chart = SimpleLineChart(800, 300, y_range=[0, max_y])

    # Chart data
    chart.add_data(supported)
    chart.add_data(totals)
    chart.add_data(alls)
    # Lowest value
    chart.add_data([0] * 2)

    # Set the line colour to blue
    chart.set_colours(["00FF00", "FF0000", "0000FF", "00000000"])

    # Set the vertical stripes
    month_stripes = 3.0
    chart.fill_linear_stripes(
        Chart.CHART,
        0,
        "ffffff",
        month_stripes / len(alls),
        "cccccc",
        month_stripes / len(alls),
    )

    # Set the horizontal dotted lines
    chart.set_grid(0, 10, 5, 5)

    chart.set_legend(
        [
            _("Supported phones").encode("utf-8"),
            _("Approved records").encode("utf-8"),
            _("Total records").encode("utf-8"),
        ]
    )

    left_axis = ["%d" % x for x in range(0, max_y + 1, int(max_y / 10))]
    left_axis[0] = ""
    chart.set_axis_labels(Axis.LEFT, left_axis)

    chart.set_axis_labels(Axis.BOTTOM, years)

    url = chart.get_url().replace("http:", "https:")
    cache.set(cache_key, url, 3600 * 24)
    return url


def phones_chart(request):
    return HttpResponseRedirect(get_chart_url())


def get_feeds():
    return [
        {
            "url": "/phones/rss/",
            "title": _("Gammu Phone Database Feed (RSS)"),
            "type": "application/rss+xml",
        },
        {
            "url": "/phones/atom/",
            "title": _("Gammu Phone Database Feed (Atom)"),
            "type": "application/atom+xml",
        },
    ]


def index(request):
    vendors = Vendor.objects.order_by("name").annotate(models_count=Count("phone"))
    phones = (
        Phone.objects.exclude(state="deleted")
        .order_by("-created")
        .prefetch_related("vendor", "features", "connection")[
            : settings.PHONES_ON_INDEX
        ]
    )
    return render(
        request,
        "phonedb/index.html",
        {
            "vendors": vendors,
            "phones": phones,
            "features": Feature.objects.all().order_by("name"),
            "chart_url": get_chart_url(),
            "feeds": get_feeds(),
            "form": SearchForm(),
        },
    )


def search(request, featurename=None):
    # We need a copy, because we might want to add a feature from URL
    rq = request.GET.copy()
    if featurename is not None:
        rq.appendlist("feature", featurename)
    form = SearchForm(rq)
    if form.is_valid():
        query = form.cleaned_data["q"]
        features = list(set(form.cleaned_data["feature"]))

        phones = Phone.objects.exclude(state="deleted").prefetch_related(
            "vendor", "features", "connection"
        )
        urlparams = []

        # Filter for features
        if len(features) > 0:
            phones = phones.filter(connection__isnull=False)
            for feature in features:
                urlparams.append("feature=%s" % feature)
                phones = phones.filter(features__name=feature)

        # Filter for query string
        if query:
            urlparams.append("q=%s" % query)
            query = query.strip()
            for part in query.split():
                phones = phones.filter(
                    Q(vendor__name__icontains=part) | Q(name__icontains=part)
                )
    else:
        phones = Phone.objects.all().prefetch_related(
            "vendor", "features", "connection"
        )
        urlparams = []

    # Sort results
    phones = phones.order_by("vendor__name", "name")

    paginator = Paginator(phones, settings.PHONES_PER_PAGE, orphans=5)
    try:
        page = int(request.GET.get("page", "1"))
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

    return render(
        request,
        "phonedb/search.html",
        {
            "phones": phones,
            "urlparams": "&".join(urlparams),
            "feeds": get_feeds(),
            "form": form,
        },
    )


@login_required
def review(request):
    phones = Phone.objects.filter(state="draft").prefetch_related(
        "vendor", "features", "connection"
    )

    # Sort results
    phones = phones.order_by("vendor__name", "name")

    paginator = Paginator(phones, settings.PHONES_PER_PAGE, orphans=5)
    try:
        page = int(request.GET.get("page", "1"))
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

    return render(
        request,
        "phonedb/search.html",
        {
            "phones": phones,
            "feeds": get_feeds(),
        },
    )


def vendor(request, vendorname):
    vendor = get_object_or_404(Vendor, slug=vendorname)
    phones = (
        Phone.objects.filter(vendor=vendor)
        .exclude(state="deleted")
        .order_by("name")
        .prefetch_related("vendor", "features", "connection")
    )

    paginator = Paginator(phones, settings.PHONES_PER_PAGE, orphans=5)
    try:
        page = int(request.GET.get("page", "1"))
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

    return render(
        request,
        "phonedb/vendor.html",
        {
            "vendor": vendor,
            "phones": phones,
            "feeds": get_feeds(),
        },
    )


def phone_redirect(request):
    try:
        pk = int(request.GET["id"])
    except Exception as error:
        raise Http404("No such entry!") from error
    phone = get_object_or_404(Phone, pk=pk)
    return HttpResponseRedirect(phone.get_absolute_url())


def phone(request, vendorname, pk):
    pk = int(pk)
    vendor = get_object_or_404(Vendor, slug=vendorname)
    phone = get_object_or_404(Phone, pk=pk, vendor=vendor)
    related = (
        Phone.objects.filter(vendor=vendor, name__icontains=phone.name)
        .exclude(pk=pk)
        .exclude(state="deleted")
        .prefetch_related("vendor", "features", "connection")
    )
    return render(
        request,
        "phonedb/phone.html",
        {
            "vendor": vendor,
            "phone": phone,
            "related": related,
            "feeds": get_feeds(),
            "user": request.user,
        },
    )


@login_required
def approve(request, vendorname, pk):
    pk = int(pk)
    vendor = get_object_or_404(Vendor, slug=vendorname)
    phone = get_object_or_404(Phone, pk=pk, vendor=vendor)

    if not request.user.is_superuser:
        return HttpResponseRedirect(phone.get_absolute_url())

    phone.state = "approved"
    phone.save()
    return HttpResponseRedirect("/phones/review/")


@login_required
def delete(request, vendorname, pk):
    pk = int(pk)
    vendor = get_object_or_404(Vendor, slug=vendorname)
    phone = get_object_or_404(Phone, pk=pk, vendor=vendor)

    if not request.user.is_superuser:
        return HttpResponseRedirect(phone.get_absolute_url())

    phone.state = "deleted"
    phone.save()
    return HttpResponseRedirect("/phones/review/")


def phones_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=gammu-phones.csv"

    writer = csv.writer(response)
    phones = (
        Phone.objects.exclude(state="deleted")
        .order_by("pk")
        .prefetch_related("vendor", "features", "connection")
    )
    writer.writerow(
        [
            "Link",
            "Manufacturer",
            "Name",
            "Author",
            "Date",
            "Connection",
            "Features",
            "Gammu-Version",
        ]
    )
    try:
        current_site = Site.objects.get_current(request)
    except Site.DoesNotExist:
        current_site = "wammu.eu"
    for phone in phones:
        if phone.connection is None:
            conn = ""
        else:
            conn = phone.connection.name
        author = phone.get_author(html=False)
        if author is None:
            author = ""
        writer.writerow(
            [
                f"https://{current_site}{phone.get_absolute_url()}",
                phone.vendor.name.encode("utf8"),
                phone.name.encode("utf8"),
                author.encode("utf8"),
                phone.created.isoformat().encode("utf8"),
                conn.encode("utf8"),
                ",".join(f.name for f in phone.features.all()).encode("utf8"),
                phone.gammu_version.encode("utf8"),
            ]
        )

    return response


@csrf_exempt
def create_wammu(request):  # noqa: C901
    """Compatibility interface for Wammu."""
    invalid = []
    version = 1
    response = HttpResponse(content_type="text/plain")

    if "irobot" not in request.POST or request.POST["irobot"] != "wammu":
        invalid.append("irobot")

    if "version" in request.POST:
        version = int(request.POST["version"])

    phone = Phone()

    try:
        phone.vendor = Vendor.objects.get(pk=int(request.POST["manufacturer"]))
    except Exception:
        invalid.append("vendor")

    try:
        phone.name = request.POST["name"]
        if len(phone.name) == 0:
            invalid.append("name")
    except Exception:
        invalid.append("name")

    try:
        phone.connection = Connection.objects.get(name=request.POST["connection"])
    except Exception:
        invalid.append("connection")

    try:
        phone.model = request.POST["model"]
        if phone.model == "auto":
            phone.model = ""
    except Exception:
        invalid.append("model")

    try:
        phone.note = request.POST["note"]
    except Exception:
        invalid.append("note")

    try:
        phone.author_name = request.POST["author_name"]
    except Exception:
        invalid.append("author_name")

    try:
        phone.author_email = request.POST["author_email"]
    except Exception:
        invalid.append("author_email")

    try:
        phone.email_garble = request.POST["email_garble"]
        if phone.email_garble not in (x[0] for x in GARBLE_CHOICES):
            invalid.append("email_garble")
    except Exception:
        invalid.append("email_garble")

    try:
        phone.gammu_version = request.POST["gammu_version"]
    except Exception:
        invalid.append("gammu_version")

    try:
        phone.full_clean()
    except ValidationError as e:
        invalid.extend(e.message_dict.keys())
        invalid = list(set(invalid))

    if len(invalid) > 0:
        response.write(INVALID % ",".join(invalid))
        return response

    features = []
    for feature in Feature.objects.all():
        key = "fts[%s]" % feature.name
        if key in request.POST and request.POST[key] == "1":
            features.append(feature)

    phone.save()

    for feature in features:
        phone.features.add(feature)

    if version == 2:
        response.write(OKAY_V2 % (phone.pk, phone.get_absolute_url()))
    else:
        response.write(OKAY % (phone.pk, phone.vendor.slug, phone.pk))
    return response


def create(request, vendorname=None):  # noqa: C901
    # Check if we did not receive legacy request
    if (
        request.method == "POST"
        and "irobot" in request.POST
        and request.POST["irobot"] == "wammu"
    ):
        return create_wammu(request)

    if (
        request.method == "POST"
        and "irobot" in request.POST
        and request.POST["irobot"] == "nospam"
    ):
        form = NewForm(request.POST)
        if form.is_valid():
            newphone = form.save()
            newphone.address = request.META.get("REMOTE_ADDR")
            if newphone.address[:7] == "::ffff:":
                newphone.address = newphone.address[7:]
            try:
                newphone.hostname = socket.gethostbyaddr(newphone.address)[0]
            except socket.herror:
                newphone.hostname = newphone.address
            newphone.save()
            messages.add_message(
                request, messages.INFO, _("Phone record has been created.")
            )
            result = HttpResponseRedirect(newphone.get_absolute_url())
            result.set_cookie(
                "phonedb_garble",
                form.cleaned_data["email_garble"].encode("utf-8"),
                max_age=3600 * 24 * 365,
            )
            result.set_cookie(
                "phonedb_author",
                form.cleaned_data["author_name"].encode("utf-8"),
                max_age=3600 * 24 * 365,
            )
            result.set_cookie(
                "phonedb_email",
                form.cleaned_data["author_email"].encode("utf-8"),
                max_age=3600 * 24 * 365,
            )
            return result
    else:
        initial = {}
        try:
            if vendorname is not None:
                vendor = Vendor.objects.get(slug=vendorname)
            else:
                vendor = Vendor.objects.get(slug=request.GET["vendor"])
            initial["vendor"] = vendor.pk
        except Exception:
            pass
        try:
            initial["name"] = request.GET["name"]
        except Exception:
            pass
        try:
            initial["email_garble"] = request.COOKIES["phonedb_garble"]
        except Exception:
            pass
        try:
            initial["author_name"] = request.COOKIES["phonedb_author"]
        except Exception:
            pass
        try:
            initial["author_email"] = request.COOKIES["phonedb_email"]
        except Exception:
            pass

        form = NewForm(initial=initial)

    return render(
        request,
        "phonedb/new.html",
        {
            "form": form,
            "feeds": get_feeds(),
        },
    )
