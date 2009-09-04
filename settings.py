# Django settings for wammu website project.
# -*- coding: UTF-8 -*-

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

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/nijel/work/gammu/wammu_web/media/'
MEDIA_ROOT = '/home/mcihar/private/wammu_web/media/'

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
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'wammu_web.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    )

TEMPLATE_DIRS = (
    '/home/mcihar/private/wammu_web/html/',
    '/home/nijel/work/gammu/wammu_web/html/',
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
    'paypal.standard.pdt',
    'wammu_web.news',
    'wammu_web.wammu',
    'wammu_web.downloads',
    'wammu_web.screenshots',
    'wammu_web.links',
    'wammu_web.manpages',
)

import gobject
import gnomekeyring
gobject.set_application_name('Wammu-web')
IDENTICA_USER = 'gammu'
IDENTICA_PASSWORD = gnomekeyring.find_network_password_sync(
        user = IDENTICA_USER,
        domain = 'identi.ca',
        protocol = 'https')[0]['password']

NEWS_PER_PAGE = 2
SCREENSHOTS_PER_PAGE = 20

PAYPAL_IDENTITY_TOKEN = '1kbDRn7TJ6ikJcqyxZ8AdOUMMT56S7gm8mq3OIHZTFS8ymCulm6IGMW70zu'
PAYPAL_RECEIVER_EMAIL = 'nijel_1251117651_biz@cihar.com'
THUMBNAIL_SIZE = (180, 180)
