import json
import os
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.dateparse import parse_datetime

from downloads.models import Download, Release, get_program

REPOSITORIES = {
    "gammu": "gammu",
    "python-gammu": "python-gammu",
    "wammu": "wammu",
}
SYNC_USERNAME = "github-release-sync"
SYNC_NAME = "Gammu release automation"
VERSION_RE = re.compile(r"\d+(?:\.\d+)+\Z")
WINDOWS_WHEEL_RE = re.compile(r"-win(?:32|_amd64|_arm64)\.whl\Z", re.IGNORECASE)
SOURCE_SUFFIXES = (".tar.gz", ".tar.bz2", ".tar.xz", ".tar.zst", ".zip")
WINDOWS_ZIP_MARKERS = ("windows", "win32", "win64", "win_amd64", "win_arm64")


class Command(BaseCommand):
    help = "imports new stable Gammu project releases from GitHub"

    def handle(self, *args, **options):
        releases_by_program = {
            program: self.fetch_releases(repository)
            for program, repository in REPOSITORIES.items()
        }

        created_releases = 0
        created_downloads = 0
        skipped_releases = 0

        with transaction.atomic():
            author = self.get_sync_user()

            for program, github_releases in releases_by_program.items():
                for github_release in reversed(github_releases):
                    result = self.import_release(program, author, github_release)
                    if result is None:
                        skipped_releases += 1
                        continue
                    created_releases += 1
                    created_downloads += result

        if created_releases:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created {created_releases} releases and "
                    f"{created_downloads} downloads; skipped "
                    f"{skipped_releases} releases.",
                ),
            )

    def fetch_releases(self, repository):
        url = f"https://api.github.com/repos/gammu/{repository}/releases?per_page=100"
        releases = []

        while url:
            self.validate_api_url(url)
            headers = {
                "Accept": "application/vnd.github+json",
                "User-Agent": "wammu.eu-release-sync",
                "X-GitHub-Api-Version": "2022-11-28",
            }
            token = os.environ.get("GITHUB_TOKEN")
            if token:
                headers["Authorization"] = f"Bearer {token}"

            request = Request(url, headers=headers)
            try:
                with urlopen(request, timeout=30) as response:  # noqa: S310
                    payload = json.loads(response.read())
                    link_header = response.headers.get("Link", "")
            except (HTTPError, URLError, OSError, json.JSONDecodeError) as error:
                raise CommandError(
                    f"Could not fetch releases for gammu/{repository}: {error}",
                ) from error

            if not isinstance(payload, list):
                raise CommandError(
                    f"Unexpected releases response for gammu/{repository}.",
                )

            releases.extend(payload)
            url = self.get_next_url(link_header)

        return releases

    @staticmethod
    def validate_api_url(url):
        parsed = urlparse(url)
        if parsed.scheme != "https" or parsed.netloc != "api.github.com":
            raise CommandError(f"Unexpected GitHub API pagination URL: {url}")

    @staticmethod
    def get_next_url(link_header):
        for link in link_header.split(","):
            target, separator, parameters = link.strip().partition(";")
            if (
                separator
                and 'rel="next"' in parameters
                and target.startswith("<")
                and target.endswith(">")
            ):
                return target[1:-1]
        return None

    @staticmethod
    def get_sync_user():
        user, created = User.objects.get_or_create(
            username=SYNC_USERNAME,
            defaults={
                "email": settings.SERVER_EMAIL,
                "first_name": SYNC_NAME,
                "is_active": False,
            },
        )
        update_fields = []
        if created:
            user.set_unusable_password()
            update_fields.append("password")
        if not user.first_name:
            user.first_name = SYNC_NAME
            update_fields.append("first_name")
        if not user.email:
            user.email = settings.SERVER_EMAIL
            update_fields.append("email")
        if update_fields:
            user.save(update_fields=update_fields)
        return user

    def import_release(self, program, author, github_release):
        if not isinstance(github_release, dict):
            raise CommandError(f"Unexpected release data for {program}.")

        if github_release.get("draft") or github_release.get("prerelease"):
            return None

        version = github_release.get("tag_name")
        if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
            self.stderr.write(
                self.style.WARNING(
                    f"Skipping {program} release with unsupported tag {version!r}.",
                ),
            )
            return None

        if Release.objects.filter(program=program, version=version).exists():
            return None

        published_at = github_release.get("published_at")
        if not isinstance(published_at, str):
            raise CommandError(f"Release {program} {version} has no publication date.")
        release_date = parse_datetime(published_at)
        if release_date is None:
            raise CommandError(
                f"Release {program} {version} has an invalid publication date.",
            )

        changelog = github_release.get("body") or ""
        if not isinstance(changelog, str):
            raise CommandError(f"Release {program} {version} has invalid notes.")

        assets = github_release.get("assets")
        if not isinstance(assets, list):
            raise CommandError(f"Release {program} {version} has invalid assets.")

        downloads = []
        for asset in assets:
            platform = self.get_asset_platform(asset)
            if platform is not None:
                downloads.append((asset, platform))

        if not downloads:
            self.stderr.write(
                self.style.WARNING(
                    f"Skipping {program} {version} because it has "
                    "no supported downloads.",
                ),
            )
            return None

        release = Release.objects.create(
            author=author,
            program=program,
            version=version,
            description="This release is available from GitHub.",
            changelog=changelog.strip(),
            date=release_date,
        )

        for asset, platform in downloads:
            self.create_download(release, platform, asset)

        self.stdout.write(
            f"Imported {get_program(program)} {version} "
            f"with {len(downloads)} downloads.",
        )
        return len(downloads)

    @staticmethod
    def get_asset_platform(asset):
        if not isinstance(asset, dict):
            raise CommandError("Unexpected GitHub release asset data.")

        name = asset.get("name")
        if not isinstance(name, str):
            raise CommandError("GitHub release asset has no name.")

        name_lower = name.lower()
        if name_lower.endswith((".exe", ".msi")) or WINDOWS_WHEEL_RE.search(name):
            return "win32"
        if name_lower.endswith(".zip") and any(
            marker in name_lower for marker in WINDOWS_ZIP_MARKERS
        ):
            return "win32"
        if name_lower.endswith(SOURCE_SUFFIXES):
            return "source"
        return None

    @staticmethod
    def create_download(release, platform, asset):
        location = asset.get("browser_download_url")
        size = asset.get("size")
        if not isinstance(location, str) or not location.startswith(
            "https://github.com/gammu/",
        ):
            raise CommandError(f"Asset {asset['name']} has an invalid download URL.")
        if not isinstance(size, int) or size < 0:
            raise CommandError(f"Asset {asset['name']} has an invalid size.")

        digest = asset.get("digest") or ""
        if not isinstance(digest, str):
            raise CommandError(f"Asset {asset['name']} has an invalid digest.")
        sha256 = digest.removeprefix("sha256:") if digest.startswith("sha256:") else ""

        Download.objects.create(
            release=release,
            platform=platform,
            location=location,
            sha256=sha256,
            size=size,
        )
