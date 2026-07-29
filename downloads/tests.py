import io
import json
from datetime import datetime
from unittest.mock import patch
from urllib.error import URLError

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.template.loader import render_to_string
from django.test import TestCase

from downloads.management.commands.sync_github_releases import (
    SYNC_NAME,
    SYNC_USERNAME,
    Command,
)
from downloads.models import Download, Release
from downloads.templatetags.getlink import getlink
from news.models import Category, Entry


def github_release(
    version="1.2.3",
    *,
    body="* Fixed an important bug.",
    assets=None,
    draft=False,
    prerelease=False,
):
    if assets is None:
        assets = []
    return {
        "tag_name": version,
        "body": body,
        "published_at": "2026-07-28T07:49:15Z",
        "draft": draft,
        "prerelease": prerelease,
        "assets": assets,
    }


def github_asset(name, *, digest="sha256:abc123", size=1024):
    return {
        "name": name,
        "browser_download_url": (
            f"https://github.com/gammu/gammu/releases/download/1.2.3/{name}"
        ),
        "digest": digest,
        "size": size,
    }


class FakeResponse(io.BytesIO):
    def __init__(self, payload, link=""):
        super().__init__(json.dumps(payload).encode())
        self.headers = {"Link": link}

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class SyncGitHubReleasesTest(TestCase):
    def setUp(self):
        for slug, title in (
            ("gammu", "Gammu"),
            ("python-gammu", "python-gammu"),
            ("wammu", "Wammu"),
        ):
            Category.objects.create(
                slug=slug,
                title=title,
                description=f"{title} news",
            )

    def run_sync(self, feeds):
        stdout = io.StringIO()
        stderr = io.StringIO()

        def fetch_releases(command, repository):
            return feeds[repository]

        with patch.object(Command, "fetch_releases", autospec=True) as fetch:
            fetch.side_effect = fetch_releases
            call_command(
                "sync_github_releases",
                stdout=stdout,
                stderr=stderr,
            )
        return stdout.getvalue(), stderr.getvalue()

    def test_imports_release_news_and_selected_assets(self):
        source = github_asset("Gammu-1.2.3.tar.gz", size=2048)
        installer = github_asset("Gammu-1.2.3-Windows.exe")
        windows_wheel = github_asset("python_gammu-1.2.3-cp313-win_amd64.whl")
        windows_zip = github_asset("Gammu-1.2.3-Windows.zip")
        source_zip = github_asset("Gammu-1.2.3.zip")
        linux_wheel = github_asset(
            "python_gammu-1.2.3-cp313-manylinux_2_28_x86_64.whl",
        )
        signature = github_asset("Gammu-1.2.3.tar.gz.asc")
        stdout, stderr = self.run_sync(
            {
                "gammu": [
                    github_release(
                        assets=[
                            source,
                            installer,
                            windows_wheel,
                            windows_zip,
                            source_zip,
                            linux_wheel,
                            signature,
                        ],
                    ),
                ],
                "python-gammu": [],
                "wammu": [],
            },
        )

        release = Release.objects.get(program="gammu", version="1.2.3")
        self.assertEqual(release.author.username, SYNC_USERNAME)
        self.assertEqual(
            release.date,
            datetime.fromisoformat("2026-07-28T07:49:15+00:00"),
        )
        self.assertEqual(release.changelog, "* Fixed an important bug.")
        self.assertEqual(
            release.description,
            "This release is available from GitHub.",
        )
        self.assertFalse(release.post_news)

        sync_user = User.objects.get(username=SYNC_USERNAME)
        self.assertFalse(sync_user.is_active)
        self.assertFalse(sync_user.has_usable_password())
        self.assertEqual(sync_user.get_full_name(), SYNC_NAME)
        self.assertEqual(sync_user.email, settings.SERVER_EMAIL)

        entry = Entry.objects.get(title="Gammu 1.2.3")
        self.assertEqual(entry.author, sync_user)
        self.assertEqual(entry.pub_date, release.date)
        self.assertEqual(
            list(entry.categories.values_list("slug", flat=True)),
            ["gammu"],
        )
        self.assertIn("* Fixed an important bug.", entry.body)

        downloads = list(release.download_set.order_by("location"))
        self.assertEqual(len(downloads), 5)
        self.assertEqual(
            {download.platform for download in downloads},
            {"source", "win32"},
        )
        self.assertEqual(
            release.download_set.get(location=source["browser_download_url"]).sha256,
            "abc123",
        )
        self.assertEqual(
            release.download_set.get(location=source["browser_download_url"]).size,
            2048,
        )
        self.assertEqual(
            release.download_set.get(
                location=windows_zip["browser_download_url"],
            ).platform,
            "win32",
        )
        self.assertEqual(
            release.download_set.get(
                location=source_zip["browser_download_url"],
            ).platform,
            "source",
        )
        self.assertIn("Created 1 releases and 5 downloads", stdout)
        self.assertEqual(stderr, "")

    def test_skips_release_without_supported_downloads(self):
        stdout, stderr = self.run_sync(
            {
                "gammu": [
                    github_release(
                        assets=[
                            github_asset(
                                "python_gammu-1.2.3-cp313-manylinux_2_28_x86_64.whl",
                            ),
                            github_asset("Gammu-1.2.3.tar.gz.asc"),
                        ],
                    ),
                ],
                "python-gammu": [],
                "wammu": [],
            },
        )

        self.assertFalse(Release.objects.exists())
        self.assertFalse(Entry.objects.exists())
        self.assertFalse(Download.objects.exists())
        self.assertIn("Created 0 releases and 0 downloads; skipped 1 releases", stdout)
        self.assertIn("no supported downloads", stderr)

    def test_sync_user_backfills_missing_display_metadata(self):
        sync_user = User.objects.create(username=SYNC_USERNAME, is_active=False)
        sync_user.set_unusable_password()
        sync_user.save(update_fields=["password"])

        sync_user = Command.get_sync_user()

        self.assertEqual(sync_user.get_full_name(), SYNC_NAME)
        self.assertEqual(sync_user.email, settings.SERVER_EMAIL)
        self.assertFalse(sync_user.has_usable_password())

    def test_skips_drafts_prereleases_invalid_tags_and_existing_releases(self):
        author = User.objects.create_user(username="maintainer")
        Release.objects.create(
            author=author,
            program="gammu",
            version="1.2.3",
            description="Existing",
            changelog="Existing",
            post_news=False,
        )

        stdout, stderr = self.run_sync(
            {
                "gammu": [
                    github_release(),
                    github_release("1.2.4", draft=True),
                    github_release("1.2.5", prerelease=True),
                    github_release("v1.2.6"),
                ],
                "python-gammu": [],
                "wammu": [],
            },
        )

        self.assertEqual(Release.objects.count(), 1)
        self.assertEqual(Entry.objects.count(), 0)
        self.assertIn("skipped 4 releases", stdout)
        self.assertIn("unsupported tag 'v1.2.6'", stderr)

    def test_existing_release_is_not_refreshed(self):
        initial = github_release(
            body="Original notes",
            assets=[github_asset("Gammu-1.2.3.tar.gz")],
        )
        self.run_sync(
            {"gammu": [initial], "python-gammu": [], "wammu": []},
        )

        changed = github_release(
            body="Changed notes",
            assets=[
                github_asset("Gammu-1.2.3.tar.gz"),
                github_asset("Gammu-1.2.3-Windows.exe"),
            ],
        )
        stdout, _stderr = self.run_sync(
            {"gammu": [changed], "python-gammu": [], "wammu": []},
        )

        release = Release.objects.get()
        self.assertEqual(release.changelog, "Original notes")
        self.assertEqual(Download.objects.count(), 1)
        self.assertEqual(Entry.objects.count(), 1)
        self.assertIn("Created 0 releases and 0 downloads", stdout)

    def test_malformed_release_rolls_back_all_imports(self):
        malformed = github_release("2.0.0")
        malformed["assets"] = None

        with self.assertRaisesMessage(CommandError, "invalid assets"):
            self.run_sync(
                {
                    "gammu": [github_release()],
                    "python-gammu": [malformed],
                    "wammu": [],
                },
            )

        self.assertFalse(Release.objects.exists())
        self.assertFalse(Entry.objects.exists())
        self.assertFalse(User.objects.filter(username=SYNC_USERNAME).exists())


class GitHubAPITest(TestCase):
    @patch(
        "downloads.management.commands.sync_github_releases.urlopen",
    )
    def test_fetches_paginated_releases(self, urlopen):
        next_url = (
            "https://api.github.com/repos/gammu/gammu/releases?per_page=100&page=2"
        )
        urlopen.side_effect = [
            FakeResponse(
                [github_release()],
                f'<{next_url}>; rel="next", <{next_url}>; rel="last"',
            ),
            FakeResponse([github_release("1.2.2")]),
        ]

        releases = Command().fetch_releases("gammu")

        self.assertEqual(
            [release["tag_name"] for release in releases], ["1.2.3", "1.2.2"]
        )
        self.assertEqual(urlopen.call_count, 2)
        request = urlopen.call_args_list[0].args[0]
        self.assertEqual(request.get_header("User-agent"), "wammu.eu-release-sync")

    @patch(
        "downloads.management.commands.sync_github_releases.urlopen",
        side_effect=URLError("offline"),
    )
    def test_api_failure_is_reported(self, urlopen):
        with self.assertRaisesMessage(CommandError, "Could not fetch releases"):
            Command().fetch_releases("gammu")
        urlopen.assert_called_once()

    @patch(
        "downloads.management.commands.sync_github_releases.urlopen",
        return_value=FakeResponse({"message": "rate limited"}),
    )
    def test_malformed_api_response_is_reported(self, urlopen):
        with self.assertRaisesMessage(CommandError, "Unexpected releases response"):
            Command().fetch_releases("gammu")
        urlopen.assert_called_once()


class DownloadRenderingTest(TestCase):
    def test_getlink_preserves_github_and_legacy_locations(self):
        github_download = Download(
            location="https://github.com/gammu/gammu/releases/download/1.2.3/file.zip",
        )
        legacy_download = Download(location="/gammu/releases/file.zip")

        self.assertEqual(getlink(github_download), github_download.location)
        self.assertEqual(
            getlink(legacy_download),
            "https://dl.cihar.com/gammu/releases/file.zip",
        )

    def test_download_list_omits_empty_checksum(self):
        author = User.objects.create_user(username="maintainer")
        release = Release.objects.create(
            author=author,
            program="gammu",
            version="1.2.3",
            description="Release",
            changelog="Changes",
            post_news=False,
        )
        Download.objects.create(
            release=release,
            platform="source",
            location=(
                "https://github.com/gammu/gammu/releases/"
                "download/1.2.3/Gammu-1.2.3.tar.gz"
            ),
            size=1024,
        )

        rendered = render_to_string(
            "downloads/dllist.html",
            {
                "downloads": release.download_set.all(),
                "program_name": "gammu",
            },
        )

        self.assertNotIn('class="checksums"', rendered)
        self.assertIn("https://github.com/gammu/gammu/releases/download/", rendered)
