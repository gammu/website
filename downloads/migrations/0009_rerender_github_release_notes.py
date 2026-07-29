import re

import markdown
from django.db import migrations

BUG_RE = re.compile("(bug ?#([0-9]*))")
ISSUE_RE = re.compile("(issue ?#([0-9]*))")
LP_RE = re.compile("(LP ?#([0-9]*))")
BDO_RE = re.compile("(bdo ?#([0-9]*))")
GITHUB_URL_RE = re.compile(
    r"(?<!<)(?<!\()(?<!\[)https://github\.com/[^\s<>]+",
)
TRAILING_URL_PUNCTUATION = ".,;:!?)]"
SYNC_USERNAME = "github-release-sync"


def process_bug_links(text):
    text = LP_RE.sub(r"[\1](https://bugs.launchpad.net/bugs/\2)", text)
    text = BDO_RE.sub(r"[\1](https://bugs.debian.org/\2)", text)
    text = ISSUE_RE.sub(r"[\1](https://github.com/gammu/gammu/\2)", text)
    return BUG_RE.sub(r"[\1](https://bugs.cihar.com/\2)", text)


def linkify_github_urls(text):
    def replace(match):
        url = match.group()
        trailing = ""
        while url[-1] in TRAILING_URL_PUNCTUATION:
            trailing = url[-1] + trailing
            url = url[:-1]
        return f"<{url}>{trailing}"

    return GITHUB_URL_RE.sub(replace, text)


def render_markdown(text):
    return markdown.markdown(linkify_github_urls(text))


def rerender_github_release_notes(apps, schema_editor):
    release_model = apps.get_model("downloads", "Release")
    entry_model = apps.get_model("news", "Entry")

    releases = release_model.objects.filter(author__username=SYNC_USERNAME)
    for release in releases.iterator():
        release.changelog_html = render_markdown(
            process_bug_links(release.changelog or ""),
        )
        release.description_html = render_markdown(release.description)
        release.save(update_fields=["changelog_html", "description_html"])

    entries = entry_model.objects.filter(author__username=SYNC_USERNAME)
    for entry in entries.iterator():
        entry.body_html = render_markdown(entry.body)
        entry.excerpt_html = (
            render_markdown(entry.excerpt) if entry.excerpt else entry.excerpt
        )
        entry.save(update_fields=["body_html", "excerpt_html"])


class Migration(migrations.Migration):
    dependencies = [
        ("downloads", "0008_github_releases"),
        ("news", "0003_auto_20210207_1428"),
    ]

    operations = [
        migrations.RunPython(
            rerender_github_release_notes,
            migrations.RunPython.noop,
        ),
    ]
