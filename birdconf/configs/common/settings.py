import logging
import os

import django

# Base paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Debugging
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Database
# Note: DATABASE_USER and DATABASE_PASSWORD are defined in the staging and
# production settings.py files. For local use, either define them in
# local_settings.py or ignore to use your local user.
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': 'localhost',
        'PORT': '5432',
        'NAME': 'birdconf',
    }
}

# Local time
TIME_ZONE = 'America/Chicago'

# Local language
LANGUAGE_CODE = 'en-gb'

# Site framework
SITE_ID = 1

# Internationalization
USE_I18N = False

# Absolute path to the directory that holds media.
MEDIA_ROOT = os.path.join(SITE_ROOT, 'assets')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'z@vza&vmrv%$hhwue3+@9os&j%ml0wi_=_wdqv^ijfjftdf-v&'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'birdconf.configs.common.urls'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth', 
    'django.contrib.contenttypes', 
    'django.contrib.messages', 
    'django.contrib.sessions',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.gis',
    'django.contrib.sitemaps',
    'playlists'
)

# Predefined domain
MY_SITE_DOMAIN = 'localhost:8000'

# Email
# run "python -m smtpd -n -c DebuggingServer localhost:1025" to see outgoing
# messages dumped to the terminal
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
DEFAULT_FROM_EMAIL = 'do.not.reply@tribune.com'

# Caching
CACHE_MIDDLEWARE_KEY_PREFIX='birdconf'
CACHE_MIDDLEWARE_SECONDS=90 * 60 # 90 minutes
CACHE_BACKEND="dummy:///"

# Analytics
OMNITURE_PAGE_NAME = "birdconf"
OMNITURE_SECTION = ""
OMNITURE_SUBSECTION = ""
GOOGLE_ANALYTICS_KEY = "UA-9792248-6"

# Logging
logging.basicConfig(
    level=logging.INFO,
)

# Allow for local (per-user) override
try:
    from local_settings import *
except ImportError:
    pass