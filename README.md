# Gammu and Wammu Website

Website for Gammu and Wammu, running at <https://wammu.eu/>.

[![Translation status](https://hosted.weblate.org/widgets/gammu/-/svg-badge.svg)](https://hosted.weblate.org/engage/gammu/?utm_source=widget)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c64ea0f982f747a9bb1e7b3b21e39f3c)](https://www.codacy.com/app/Gammu/website)
[![Code Health](https://landscape.io/github/gammu/website/master/landscape.svg?style=flat)](https://landscape.io/github/gammu/website/master)
[![Build Status](https://travis-ci.org/gammu/website.svg?branch=master)](https://travis-ci.org/gammu/website)
[![codecov](https://codecov.io/gh/gammu/website/branch/master/graph/badge.svg)](https://codecov.io/gh/gammu/website)

## Release synchronization

Run `./manage.py sync_github_releases` from cron to import new stable Gammu,
python-gammu, and Wammu releases from GitHub. The command can use an optional
`GITHUB_TOKEN` environment variable to increase the GitHub API rate limit.

The synchronization backfills missing releases and does not update releases
that are already present on the website.
