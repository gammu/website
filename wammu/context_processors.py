# Context processors


from django.utils import timezone
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
            {"url": f"https://cs.wammu.eu{path}", "name": "Česky", "code": "cs"},
        )

    if lang != "en":
        langs.append(
            {"url": f"https://wammu.eu{path}", "name": "English", "code": "en"},
        )

    if lang != "es":
        langs.append(
            {"url": f"https://es.wammu.eu{path}", "name": "Español", "code": "es"},
        )

    if lang != "de":
        langs.append(
            {"url": f"https://de.wammu.eu{path}", "name": "Deutsch", "code": "de"},
        )

    if lang != "ru":
        langs.append(
            {"url": f"https://ru.wammu.eu{path}", "name": "Русский", "code": "ru"},
        )

    if lang != "sk":
        langs.append(
            {"url": f"https://sk.wammu.eu{path}", "name": "Slovenčina", "code": "sk"},
        )

    if lang != "fr":
        langs.append(
            {"url": f"https://fr.wammu.eu{path}", "name": "Français", "code": "fr"},
        )

    if lang != "pt-br":
        langs.append(
            {
                "url": f"https://pt-br.wammu.eu{path}",
                "name": "Português brasileiro",
                "code": "pt-BR",
            },
        )

    return {"translations": langs}


def dates(request):
    return {
        "current_year": timezone.now().strftime("%Y"),
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
        ],
    }


def data(request):
    return {
        "news_categories": Category.objects.all(),
        "screenshot_categories": ScreenshotCategory.objects.all(),
    }
