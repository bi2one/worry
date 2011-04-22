import os

# Django settings for worry project.
FORCE_SCRIPT_NAME = ''
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'dontworry'             # Or path to database file if using sqlite3.
DATABASE_USER = 'dontworry'             # Not used with sqlite3.
DATABASE_PASSWORD = 'worryworry'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Seoul'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ko'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'site_media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'


# APPEND_SLASH=False


# CACHE 
CACHE_BACKEND = 'memcached://127.0.0.1:11211'
CACHE_MIDDLEWARE_SECONDS = 60 * 3
CACHE_MIDDLEWARE_ANONYMOUS_ONLY=True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'jqv)0_^fv(4v6wqqmpwm+71oz(ic2j)js$&4$e1)mlg=e3&aui'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)


SESSION_EXPIRE_AT_BROWSER_CLOSE=True

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.cache.CacheMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

# TEMPLATE_CONTEXT_PROCESSORS = (
#      'django.core.context_processors.request',
# )


ROOT_URLCONF = 'worry.urls'
UPLOAD_DIR = os.path.join('/Users/bi2one/public_html/worry/site_media/upload/')
# UPLOAD_DIR = os.path.join('/home/worry/worry/site_media/upload/')
# UPLOAD_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '/site_media/upload/')
RESIZE_SIZE = 570
THUMB_SIZE = 128

FILE_TYPE=1
IMAGE_TYPE=2



TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates'),
)

MODULE_ID = {'blog':1, 'board':2, 'guest':3}

BLOG_CATEGORY_NAME = {1:'allak', 2:'worry'}

BOARD_CATEGORY_NAME = {1:'worryboard',2:'shop',3:'notice',4:'faq'}


BLOG_CATEGORY_ID = {'allak' :1, 'worry' :2}

BOARD_CATEGORY_ID = {'worryboard' :1, 'shop' :2, 'notice' : 3, 'faq' : 4}

############## using in twitter app
MODULE_NAMES = ['blog', 'worryboard', 'shop', 'notice', 'faq', 'guest']

TWITTER_ACCESS_TOKEN_STRING = 'oauth_token_secret=JfZJvXa2BRoLUTdzRN3KTNXo7zxEgn2GHZuXcXBk&oauth_token=113097297-N1c5cPACMLQgDzBrdEMw5PNXLIMrLbpASgN3VGWD'
BITLY_LOGIN = 'mgsmurf'
BITLY_APIKEY = 'R_6257823867f1f0bb5d81310005a38280'
##############

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'worry.document.templatetags',
    'worry.document',
    'worry.worry_admin',
    'worry.twitter',
    'worry.file_manager',
    'worry.accounts',
    'worry.order',
)
