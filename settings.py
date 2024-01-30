# Django settings for wammu website project.

import os

from django.http import Http404

DEBUG = True

ADMINS = (("Michal Čihař", "michal@cihar.com"),)

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        "NAME": "./wammu.db",  # Or path to database file if using sqlite3.
        "USER": "",  # Not used with sqlite3.
        "PASSWORD": "",  # Not used with sqlite3.
        "HOST": "",  # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "",  # Set to empty string for default. Not used with sqlite3.
    },
}

WEB_ROOT = os.path.dirname(os.path.abspath(__file__))

FILES_ROOT = "/srv/http/dl.cihar.com/"

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "Europe/Prague"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en"

LANGUAGES = (
    ("cs", "Čeština"),
    ("de", "Deutsch"),
    ("en", "English"),
    ("es", "Español"),
    ("fr", "Français"),
    ("pt-br", "Português brasileiro"),
    ("ru", "Русский"),
    ("sk", "Slovenčina"),
)

LOCALE_PATHS = ("%s/locale" % WEB_ROOT,)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = "%s/media/" % WEB_ROOT

HTML_ROOT = "%s/html/" % WEB_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = ""

# URL prefix for static files.
STATIC_URL = "/static/"

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
ADMIN_MEDIA_PREFIX = "/static/admin/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = "c=kt_6vtz&(418w-0(uti(q5&e76q#lc=%vuwzm&+ulqrkgyp3"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wammu.middleware.SiteLocaleMiddleware",
    "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
]

ROLLBAR = {
    "access_token": "",
    "environment": "development" if DEBUG else "production",
    "branch": "master",
    "root": "/home/nijel/wammu/",
    "exception_level_filters": [
        (Http404, "ignored"),
    ],
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

ROOT_URLCONF = "urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            HTML_ROOT,
        ],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.csrf",
                "django.contrib.messages.context_processors.messages",
                "wammu.context_processors.translations",
                "wammu.context_processors.dates",
                "wammu.context_processors.feeds",
                "wammu.context_processors.data",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "crispy_forms",
    "crispy_bootstrap3",
    "news",
    "wammu",
    "downloads",
    "screenshots",
    "links",
    "phonedb",
    "tools",
)

NEWS_PER_PAGE = 5
NEWS_ON_MAIN_PAGE = 5
NEWS_ON_PRODUCT_PAGE = 2
NEWS_IN_RSS = 10
SCREENSHOTS_PER_PAGE = 20
PHONES_PER_PAGE = 50
PHONES_ON_INDEX = 10
PHONES_ON_MAIN_PAGE = 5
PHONES_IN_RSS = 10

THUMBNAIL_SIZE = (180, 180)

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap3"
CRISPY_TEMPLATE_PACK = "bootstrap3"

SEND_BROKEN_LINK_EMAILS = True
SERVER_EMAIL = "django@wammu.eu"

CACHE_BACKEND = "db://cache"

DEFAULT_CONTENT_TYPE = "application/xhtml+xml"
DEFAULT_CONTENT_TYPE = "text/html"
DEFAULT_CHARSET = "utf-8"

# Use etags based caching
USE_ETAGS = True

IGNORABLE_404_ENDS = [
    "logo.png",
    "logo_001.png",
    "piwik.js",
    "piwik.js/",
    "piwik.php",
    "michal@cihar.com",
    "piwik.php/",
]
IGNORABLE_404_STARTS = ["/plugins/editors/tinymce", "/cgi-bin/"]

EMAIL_SUBJECT_PREFIX = "[wammu.eu] "

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "wammu.eu",
    "cs.wammu.eu",
    "de.wammu.eu",
    "es.wammu.eu",
    "fr.wammu.eu",
    "pt-br.wammu.eu",
    "ru.wammu.eu",
    "sk.wammu.eu",
]

X_FRAME_OPTIONS = "DENY"

if DEBUG:
    INSTALLED_APPS += ("debug_toolbar",)
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ("127.0.0.1",)
