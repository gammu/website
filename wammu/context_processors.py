# Context processors

from datetime import datetime

from django.utils.translation import get_language
from django.utils.translation import gettext as _

from news.models import Category
from screenshots.models import Category as ScreenshotCategory


def translations(request):
    path = request.get_full_path()
    langs = []

    lang = get_language()

    if lang != "cs":
        langs.append(
            {"url": "https://cs.wammu.eu%s" % path, "name": "Česky", "code": "cs"}
        )

    if lang != "en":
        langs.append(
            {"url": "https://wammu.eu%s" % path, "name": "English", "code": "en"}
        )

    if lang != "es":
        langs.append(
            {"url": "https://es.wammu.eu%s" % path, "name": "Español", "code": "es"}
        )

    if lang != "de":
        langs.append(
            {"url": "https://de.wammu.eu%s" % path, "name": "Deutsch", "code": "de"}
        )

    if lang != "ru":
        langs.append(
            {"url": "https://ru.wammu.eu%s" % path, "name": "Русский", "code": "ru"}
        )

    if lang != "sk":
        langs.append(
            {"url": "https://sk.wammu.eu%s" % path, "name": "Slovenčina", "code": "sk"}
        )

    if lang != "fr":
        langs.append(
            {"url": "https://fr.wammu.eu%s" % path, "name": "Français", "code": "fr"}
        )

    if lang != "pt-br":
        langs.append(
            {
                "url": "https://pt-br.wammu.eu%s" % path,
                "name": "Português brasileiro",
                "code": "pt-BR",
            }
        )

    return {"translations": langs}


def dates(request):
    return {
        "current_year": datetime.now().strftime("%Y"),
    }


def feeds(request):
    return {
        "global_feeds": [
            {
                "url": "/news/rss/",
                "title": _("Gammu and Wammu News Feed (RSS)"),
                "type": "application/rss+xml",
            },
            {
                "url": "/news/atom/",
                "title": _("Gammu and Wammu News Feed (Atom)"),
                "type": "application/atom+xml",
            },
        ]
    }


def data(request):
    return {
        "news_categories": Category.objects.all(),
        "screenshot_categories": ScreenshotCategory.objects.all(),
    }
