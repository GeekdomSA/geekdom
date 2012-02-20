import os.path
from local_settings import *

TEMPLATE_DEBUG = DEBUG
MANAGERS = ADMINS
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5)(n613$1+q=i183(f5*=b3y7#g_)t*$cigb-yu+7mz-$d0v_3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    # 'geekdom.manager.processors.flickr_background',
    'geekdom.manager.processors.all_users',
    'geekdom.manager.processors.check_for_checkin_cookie',
    'geekdom.manager.processors.cta_banner',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'manager.middleware.CheckinChecker',
)

ROOT_URLCONF = 'geekdom.urls'

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'geekdom.manager',
    'uni_form',
    'easy_thumbnails',
    'pagination',
    'geekdom.userena',
    'guardian',
    'bootstrapform',
)

AUTH_PROFILE_MODULE = 'manager.UserProfile'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# required userena settings


AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'

ANONYMOUS_USER_ID = 1


FOURSQUARE_CLIENT_ID = "YLKQCPEJCFMQPAQ3TRZQNBJV4HVNFLGLIFNNE5UO2QZRRL2T"
FOURSQUARE_CLIENT_SECRET = "UHF0P1MOEKEJQGYDVWWUNERERFODWMFG3WIL2LLR2DSHGV4Y"
FOURSQUARE_VENUE_ID = "4e9700536da11364e6ee330d"
FOURSQUARE_OAUTH_TOKEN = "WUWNSAI4JGTU103CFGRFN3BKLEK0XHQGOJFS03BJSRDEGHAF"
FOURSQUARE_VERSION = "20120101"
FOURSQUARE_REDIRECT_URL = "http://members.geekdom.com"

# userless auth code
# &client_id=YLKQCPEJCFMQPAQ3TRZQNBJV4HVNFLGLIFNNE5UO2QZRRL2T&client_secret=UHF0P1MOEKEJQGYDVWWUNERERFODWMFG3WIL2LLR2DSHGV4Y&v=20120101




# userena settings
USERENA_DEFAULT_PRIVACY = "open"
USERENA_WITHOUT_USERNAMES = True
