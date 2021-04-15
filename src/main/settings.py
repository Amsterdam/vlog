import os
from distutils.util import strtobool

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", False)

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_extensions",
    "contrib.timescale",
    "django_prometheus",
    "vlog",
    "reistijden_v1",
    "api",
    "ingress",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
    "django_sentry_400_middleware.Sentry400CatchMiddleware",
]

ROOT_URLCONF = "main.urls"
BASE_URL = os.getenv("BASE_URL", "/")
FORCE_SCRIPT_NAME = BASE_URL

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "main.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "contrib.timescale.db.backend",
        "NAME": os.getenv("DATABASE_NAME", "dev"),
        "USER": os.getenv("DATABASE_USER", "dev"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", "dev"),
        "HOST": os.getenv("DATABASE_HOST", "database"),
        "PORT": os.getenv("DATABASE_PORT", "5432"),
        "CONN_MAX_AGE": float(os.getenv("DATABASE_CONN_MAX_AGE", 20)),
    }
}

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "contrib.rest_framework.authentication.SimpleTokenAuthentication",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "contrib.rest_framework.parsers.PlainTextParser",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "contrib.rest_framework.renderers.PlainTextRenderer",
    ],
    "TEST_REQUEST_RENDERER_CLASSES": [
        "rest_framework_xml.renderers.XMLRenderer",
        "rest_framework.renderers.JSONRenderer",
        "contrib.rest_framework.renderers.PlainTextRenderer",
    ],
}


# A list of classpaths to implementations of ingress.consumer.IngressConsumer
# to handle the data in the queue.
INGRESS_CONSUMER_CLASSES = ["reistijden_v1.consumer.ReistijdenConsumer"]

# A list of authentication classes used in the ingress view.
# See https://www.django-rest-framework.org/api-guide/authentication/
INGRESS_AUTHENTICATION_CLASSES = [
    "contrib.rest_framework.authentication.SimpleTokenAuthentication",
]

# A list of permission classes used in the ingress view.
# See https://www.django-rest-framework.org/api-guide/permissions/
INGRESS_PERMISSION_CLASSES = [
    "rest_framework.permissions.IsAuthenticated",
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = os.path.join(BASE_URL, "static/")
STATIC_ROOT = "static"

# The token that is allowed to post data to protected endpoints
AUTHORIZATION_TOKEN = os.getenv("AUTHORIZATION_TOKEN")

if os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        integrations=[DjangoIntegration()],
        ignore_errors=["ExpiredSignatureError"],
        request_bodies='always',
    )

# Prometheus
prometheus_dir = os.getenv("prometheus_multiproc_dir")
if prometheus_dir and not os.path.exists(prometheus_dir):
    os.makedirs(prometheus_dir)
