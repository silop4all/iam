"""
Django settings for IdentityAccessManager project.
"""
from os import path
PROJECT_ROOT = path.dirname(path.abspath(path.dirname(__file__)))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

HOST = {
    'PROTOCOL': "http",
    'IP': "192.168.1.2", 
    'PORT': 80,
    'PATH': '/prosperity4all/identity-access-manager'
}

ALLOWED_HOSTS = (
    '*',
)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

OPENAM_HOST = "http://192.168.1.3/openam/"
OPENAM = {
    'PROTOCOL': "http",
    'IP': "192.168.1.3", 
    'PORT': 80
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'openam',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

LOGIN_URL = '/login'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''
MEDIA_ROOT = path.join(PROJECT_ROOT, 'media').replace('\\', '/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
#MEDIA_URL = ''
MEDIA_URL = '/prosperity4all/identity-access-manager/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = path.join(PROJECT_ROOT, 'static').replace('\\', '/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/prosperity4all/identity-access-manager/static/'


# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'n(bd1f1c%e8=_xad02x5qtfn%wgwpi492e$8_erx+d)!tpeoim'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.common.CommonMiddleware', 
    # django debug tools
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'app.middleware.token_validation.TokenValidationMiddleware',
)

ROOT_URLCONF = 'IdentityAccessManager.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'IdentityAccessManager.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'restapi',
    'rest_framework',
    'rest_framework_swagger',
    'corsheaders',
    #'debug_toolbar',
    'analytical',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] - [%(name)s:%(lineno)s] - [%(levelname)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(PROJECT_ROOT) + "/logs/error.log",
            'maxBytes': 2024 * 2024,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'apifile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(PROJECT_ROOT) + "/logs/api_error.log",
            'maxBytes': 2024 * 2024,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'app': {
            'handlers': ['logfile'],
            'level': 'INFO',
        },
        'restapi': {
            'handlers': ['apifile'],
            'level': 'INFO',
        },

    }
}


# Specify the default test runner.
TEST_RUNNER = 'django.test.runner.DiscoverRunner'


# Django rest framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        'rest_framework.permissions.AllowAny',
    ],
    #'DEFAULT_FILTER_BACKENDS': (
    #    'rest_framework.filters.DjangoFilterBackend',
    #),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}



# Settings for swagger
SWAGGER_SETTINGS = {
    'exclude_namespaces': ['private_api'],
    'api_version': '1.0',
    'api_path': '/',
    'base_path': str(HOST['IP']) + ":" + str(HOST['PORT']) + str(HOST['PATH']) + '/docs',
    'enabled_methods': [
        'get',
        'post',
        'put',
        'patch',
        'delete',
        'options'
    ],
    'api_key': '',
    'is_authenticated': False,
    'is_superuser': False,
    'unauthenticated_user': 'django.contrib.auth.models.AnonymousUser',
    #'permission_denied_handler': None,
    #'resource_access_handler': None,
    'info': {
        'contact': 'yyyyyyyyyyyyyyy@gmail.com',
        'description': 'This project has received funding from the European Union\'s Seventh Programme for research, technological development and demonstration under grant agreement, No 610510. Find below the documentation of REST web services that OpenAM plugin provides.',
        'license': 'Apache 2.0',
        'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        'title': 'Prosperity4All project: documentation of Identity & Access Manager web services',
    },
    'doc_expansion': 'none',
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)

# Email account for notifications
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_HOST_USER     = 'xxxxxxxxxxxxx@gmail.com'
EMAIL_HOST_PASSWORD = 'xxxxxxxxxxxxx'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True


# Google analytics
GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-78801534-1'
ANALYTICAL_INTERNAL_IPS = ['192.168.1.8']
ANALYTICAL_AUTO_IDENTIFY = False
GOOGLE_ANALYTICS_DISPLAY_ADVERTISING = True