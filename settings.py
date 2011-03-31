# Django settings for wammu website project.
# -*- coding: UTF-8 -*-

from socket import gethostname

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Michal Čihař', 'michal@cihar.com'),
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = './wammu.db'   # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Prague'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

HOSTNAME = gethostname()
if HOSTNAME == 'rincewind':
    WEB_ROOT = '/home/mcihar/private/wammu_web/'
elif HOSTNAME == 'raptor':
    WEB_ROOT = '/home/nijel/work/gammu/wammu_web/'
elif HOSTNAME == 'web':
    WEB_ROOT = '/var/lib/django/wammu_web/'
else:
    WEB_ROOT = '/home/nijel/work/gammu/wammu_web/'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '%s/media/' % WEB_ROOT

HTML_ROOT= '%s/html/' % WEB_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'c=kt_6vtz&(418w-0(uti(q5&e76q#lc=%vuwzm&+ulqrkgyp3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
#    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
#    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
    'wammu.context_processors.translations',
    'wammu.context_processors.menu',
    'wammu.context_processors.message',
    'wammu.context_processors.dates',
    'wammu.context_processors.feeds',
    )

TEMPLATE_DIRS = (
    HTML_ROOT,
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',
    'news',
    'wammu',
    'downloads',
    'screenshots',
    'links',
    'phonedb',
    'tools',
)

#import gobject
#import gnomekeyring
#gobject.set_application_name('Wammu-web')
IDENTICA_USER = 'gammu'
IDENTICA_PASSWORD = ''
#IDENTICA_PASSWORD = gnomekeyring.find_network_password_sync(
#        user = IDENTICA_USER,
#        domain = 'identi.ca',
#        protocol = 'https')[0]['password']

NEWS_PER_PAGE = 5
NEWS_ON_MAIN_PAGE = 5
NEWS_ON_PRODUCT_PAGE = 2
NEWS_IN_RSS = 10
SCREENSHOTS_PER_PAGE = 20
PHONES_PER_PAGE = 50
PHONES_ON_INDEX = 10
PHONES_ON_MAIN_PAGE = 5
PHONES_IN_RSS = 10

PAYPAL_IDENTITY_TOKEN = '1kbDRn7TJ6ikJcqyxZ8AdOUMMT56S7gm8mq3OIHZTFS8ymCulm6IGMW70zu'
PAYPAL_RECEIVER_EMAIL = 'nijel_1251117651_biz@cihar.com'
THUMBNAIL_SIZE = (180, 180)

SEND_BROKEN_LINK_EMAILS = True
SERVER_EMAIL = 'django@wammu.eu'

CACHE_BACKEND = 'db://cache'

DEFAULT_CONTENT_TYPE = 'application/xhtml+xml'
DEFAULT_CONTENT_TYPE = 'text/html'
DEFAULT_CHARSET = 'utf-8'

# Use etags based caching
USE_ETAGS = True

IGNORABLE_404_ENDS = ['logo.png', 'logo_001.png', 'piwik.js', 'piwik.js/', 'piwik.php', 'michal@cihar.com', 'piwik.php/']
IGNORABLE_404_STARTS = ['/plugins/editors/tinymce', '/cgi-bin/']
