import contextlib
import csv
import socket

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.db.models import Count, Q
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt

from phonedb.charts import get_phone_records_chart
from phonedb.forms import NewForm, SearchForm
from phonedb.models import GARBLE_CHOICES, Connection, Feature, Phone, Vendor

# API responses, need to stay for Wammu compatibility
INVALID = "Invalid values: %s"
OKAY = "Entry created, id=%d, url=/gammu/phonedb/%s/%d"
OKAY_V2 = "Entry created, id=%d, url=%s"


def phones_chart(request):
    return HttpResponse(get_phone_records_chart(), content_type="image/svg+xml")


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
            "vendor",
            "features",
            "connection",
        )
        urlparams = []

        # Filter for features
        if len(features) > 0:
            phones = phones.filter(connection__isnull=False)
            for feature in features:
                urlparams.append(f"feature={feature}")
                phones = phones.filter(features__name=feature)

        # Filter for query string
        if query:
            urlparams.append(f"q={query}")
            query = query.strip()
            for part in query.split():
                phones = phones.filter(
                    Q(vendor__name__icontains=part) | Q(name__icontains=part),
                )
    else:
        phones = Phone.objects.all().prefetch_related(
            "vendor",
            "features",
            "connection",
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
        "vendor",
        "features",
        "connection",
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
    except (KeyError, ValueError) as error:
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
        ],
    )
    try:
        current_site = Site.objects.get_current(request)
    except Site.DoesNotExist:
        current_site = "wammu.eu"
    for phone in phones:
        conn = "" if phone.connection is None else phone.connection.name
        author = phone.get_author(html=False)
        if author is None:
            author = ""
        writer.writerow(
            [
                f"https://{current_site}{phone.get_absolute_url()}",
                phone.vendor.name,
                phone.name,
                author,
                phone.created.isoformat(),
                conn,
                ",".join(f.name for f in phone.features.all()),
                phone.gammu_version,
            ],
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
    except (KeyError, ValueError, Vendor.DoesNotExist):
        invalid.append("vendor")

    try:
        phone.name = request.POST["name"]
        if len(phone.name) == 0:
            invalid.append("name")
    except KeyError:
        invalid.append("name")

    try:
        phone.connection = Connection.objects.get(name=request.POST["connection"])
    except (KeyError, Connection.DoesNotExist):
        invalid.append("connection")

    try:
        phone.model = request.POST["model"]
        if phone.model == "auto":
            phone.model = ""
    except KeyError:
        invalid.append("model")

    try:
        phone.note = request.POST["note"]
    except KeyError:
        invalid.append("note")

    try:
        phone.author_name = request.POST["author_name"]
    except KeyError:
        invalid.append("author_name")

    try:
        phone.author_email = request.POST["author_email"]
    except KeyError:
        invalid.append("author_email")

    try:
        phone.email_garble = request.POST["email_garble"]
        if phone.email_garble not in (x[0] for x in GARBLE_CHOICES):
            invalid.append("email_garble")
    except KeyError:
        invalid.append("email_garble")

    try:
        phone.gammu_version = request.POST["gammu_version"]
    except KeyError:
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
        key = f"fts[{feature.name}]"
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


def create(request, vendorname=None):
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
                request,
                messages.INFO,
                _("Phone record has been created."),
            )
            result = HttpResponseRedirect(newphone.get_absolute_url())
            result.set_cookie(
                "phonedb_garble",
                form.cleaned_data["email_garble"],
                max_age=3600 * 24 * 365,
            )
            result.set_cookie(
                "phonedb_author",
                form.cleaned_data["author_name"],
                max_age=3600 * 24 * 365,
            )
            result.set_cookie(
                "phonedb_email",
                form.cleaned_data["author_email"],
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
        except (KeyError, Vendor.DoesNotExist, Vendor.MultipleObjectsReturned):
            pass
        with contextlib.suppress(Exception):
            initial["name"] = request.GET["name"]
        with contextlib.suppress(Exception):
            initial["email_garble"] = request.COOKIES["phonedb_garble"]
        with contextlib.suppress(Exception):
            initial["author_name"] = request.COOKIES["phonedb_author"]
        with contextlib.suppress(Exception):
            initial["author_email"] = request.COOKIES["phonedb_email"]

        form = NewForm(initial=initial)

    return render(
        request,
        "phonedb/new.html",
        {
            "form": form,
            "feeds": get_feeds(),
        },
    )
