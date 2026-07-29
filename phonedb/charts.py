import bisect
import datetime
import xml.etree.ElementTree as ET

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone, translation
from django.utils.translation import gettext as _

from phonedb.models import Phone

CHART_WIDTH = 800
CHART_HEIGHT = 300
PLOT_LEFT = 45
PLOT_TOP = 18
PLOT_WIDTH = 565
PLOT_HEIGHT = 240
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
FONT_FAMILY = "system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"


def _format_number(value):
    return f"{value:.2f}".rstrip("0").rstrip(".")


def _add_element(parent, tag, **attributes):
    return ET.SubElement(
        parent,
        tag,
        {
            name.removesuffix("_").replace("_", "-"): str(value)
            for name, value in attributes.items()
        },
    )


def _get_series():
    return (
        ("supported-phones", _("Supported phones"), "#009e73"),
        ("approved-records", _("Approved records"), "#b7791f"),
        ("total-records", _("Total records"), "#0072b2"),
    )


def _get_chart_data():
    now = timezone.now()
    boundaries = []
    years = []
    for year in range(2006, now.year + 1):
        last_month = now.month if year == now.year else 12
        for month in range(1, last_month + 1):
            boundaries.append(
                datetime.datetime(year, month, 1, tzinfo=datetime.timezone.utc),
            )
            years.append(str(year) if month == 1 else "")

    all_dates = []
    approved_dates = []
    supported_dates = []
    chart_start = datetime.datetime(1900, 1, 1, tzinfo=datetime.timezone.utc)
    for created, state, connection_id in Phone.objects.values_list(
        "created",
        "state",
        "connection_id",
    ):
        all_dates.append(created)
        if state != "deleted" and created >= chart_start:
            approved_dates.append(created)
            if connection_id is not None:
                supported_dates.append(created)

    all_dates.sort()
    approved_dates.sort()
    supported_dates.sort()

    supported = [
        bisect.bisect_right(supported_dates, boundary) for boundary in boundaries
    ]
    approved = [
        bisect.bisect_right(approved_dates, boundary) for boundary in boundaries
    ]
    totals = [bisect.bisect_left(all_dates, boundary) for boundary in boundaries]
    max_y = (max(totals, default=0) // 100 + 1) * 100
    return (supported, approved, totals), years, max_y


def _render_chart(series_values, years, max_y):
    series = _get_series()
    root = ET.Element(
        "svg",
        {
            "xmlns": SVG_NAMESPACE,
            "width": str(CHART_WIDTH),
            "height": str(CHART_HEIGHT),
            "viewBox": f"0 0 {CHART_WIDTH} {CHART_HEIGHT}",
            "role": "img",
            "aria-labelledby": "chart-title",
        },
    )
    title = _add_element(root, "title", id="chart-title")
    title.text = _("Phone Records Summary")

    _add_element(
        root,
        "rect",
        width=CHART_WIDTH,
        height=CHART_HEIGHT,
        fill="#ffffff",
    )

    definitions = _add_element(root, "defs")
    clip_path = _add_element(definitions, "clipPath", id="plot-area")
    _add_element(
        clip_path,
        "rect",
        x=PLOT_LEFT,
        y=PLOT_TOP,
        width=PLOT_WIDTH,
        height=PLOT_HEIGHT,
    )

    data_length = len(years)
    x_step = PLOT_WIDTH / max(data_length - 1, 1)
    _add_element(
        root,
        "rect",
        x=PLOT_LEFT,
        y=PLOT_TOP,
        width=PLOT_WIDTH,
        height=PLOT_HEIGHT,
        fill="#fbfcfd",
    )
    stripes = _add_element(root, "g", clip_path="url(#plot-area)")
    for start in range(3, data_length, 6):
        stripe_x = PLOT_LEFT + start * x_step
        _add_element(
            stripes,
            "rect",
            x=_format_number(stripe_x),
            y=PLOT_TOP,
            width=_format_number(3 * x_step),
            height=PLOT_HEIGHT,
            fill="#f1f3f5",
        )

    grid = _add_element(
        root,
        "g",
        stroke="#d7dce2",
        stroke_width=0.75,
        stroke_dasharray="3 4",
    )
    for step in range(11):
        y = PLOT_TOP + PLOT_HEIGHT - step * PLOT_HEIGHT / 10
        _add_element(
            grid,
            "line",
            x1=PLOT_LEFT,
            y1=_format_number(y),
            x2=PLOT_LEFT + PLOT_WIDTH,
            y2=_format_number(y),
        )
        if step:
            label = _add_element(
                root,
                "text",
                x=PLOT_LEFT - 6,
                y=_format_number(y + 3),
                text_anchor="end",
                font_family=FONT_FAMILY,
                font_size=10,
                fill="#4b5563",
            )
            label.text = str(max_y * step // 10)

    axes = _add_element(root, "g", stroke="#7b8490", stroke_width=1)
    _add_element(
        axes,
        "line",
        x1=PLOT_LEFT,
        y1=PLOT_TOP,
        x2=PLOT_LEFT,
        y2=PLOT_TOP + PLOT_HEIGHT,
    )
    _add_element(
        axes,
        "line",
        x1=PLOT_LEFT,
        y1=PLOT_TOP + PLOT_HEIGHT,
        x2=PLOT_LEFT + PLOT_WIDTH,
        y2=PLOT_TOP + PLOT_HEIGHT,
    )

    for index, year in enumerate(years):
        if not year:
            continue
        label = _add_element(
            root,
            "text",
            x=_format_number(PLOT_LEFT + index * x_step),
            y=PLOT_TOP + PLOT_HEIGHT + 16,
            text_anchor="middle",
            font_family=FONT_FAMILY,
            font_size=10,
            fill="#4b5563",
        )
        label.text = year

    lines = _add_element(root, "g", clip_path="url(#plot-area)")
    for (class_name, _label, colour), values in zip(
        series,
        series_values,
        strict=True,
    ):
        points = []
        for index, value in enumerate(values):
            x = PLOT_LEFT + index * x_step
            y = PLOT_TOP + PLOT_HEIGHT * (1 - value / max_y)
            points.append(f"{_format_number(x)},{_format_number(y)}")
        _add_element(
            lines,
            "polyline",
            class_=f"series {class_name}",
            points=" ".join(points),
            fill="none",
            stroke=colour,
            stroke_width=2.5,
            stroke_linecap="round",
            stroke_linejoin="round",
        )

    legend_x = PLOT_LEFT + PLOT_WIDTH + 25
    for index, (_class_name, label_text, colour) in enumerate(series):
        y = PLOT_TOP + 20 + index * 24
        _add_element(
            root,
            "line",
            x1=legend_x,
            y1=y,
            x2=legend_x + 20,
            y2=y,
            stroke=colour,
            stroke_width=3,
            stroke_linecap="round",
        )
        label = _add_element(
            root,
            "text",
            x=legend_x + 28,
            y=y + 4,
            font_family=FONT_FAMILY,
            font_size=11,
            font_weight=600,
            fill="#374151",
        )
        label.text = label_text

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def render_phone_records_chart():
    return _render_chart(*_get_chart_data())


def get_phone_records_chart(force=False):
    language = translation.get_language() or settings.LANGUAGE_CODE
    cache_key = f"phonedb-chart-svg-{language}"
    chart = cache.get(cache_key)
    if chart is None or force:
        chart = render_phone_records_chart()
        cache.set(cache_key, chart, 24 * 60 * 60)
    return chart
