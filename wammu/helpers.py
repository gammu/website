import re

import markdown

BUG_RE = re.compile("(bug ?#([0-9]*))")
ISSUE_RE = re.compile("(issue ?#([0-9]*))")
LP_RE = re.compile("(LP ?#([0-9]*))")
BDO_RE = re.compile("(bdo ?#([0-9]*))")
GITHUB_URL_RE = re.compile(
    r"(?<!<)(?<!\()(?<!\[)https://github\.com/[^\s<>]+",
)
TRAILING_URL_PUNCTUATION = ".,;:!?)]"


def process_bug_links(text):
    """Makes links in form bug #123 clickable to bugs.cihar.com."""
    text = LP_RE.sub(r"[\1](https://bugs.launchpad.net/bugs/\2)", text)
    text = BDO_RE.sub(r"[\1](https://bugs.debian.org/\2)", text)
    text = ISSUE_RE.sub(r"[\1](https://github.com/gammu/gammu/\2)", text)
    return BUG_RE.sub(r"[\1](https://bugs.cihar.com/\2)", text)


def linkify_github_urls(text):
    """Makes bare GitHub URLs compatible with Python-Markdown autolinking."""

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
