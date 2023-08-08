"""Production settings and globals."""
from urllib.parse import urlparse
import ssl
import certifi

import dj_database_url
from urllib.parse import urlparse

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from .common import *  # noqa

# Database
DEBUG = int(os.environ.get("DEBUG", 0)) == 1

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "plane",
        "USER": os.environ.get("PGUSER", ""),
        "PASSWORD": os.environ.get("PGPASSWORD", ""),
        "HOST": os.environ.get("PGHOST", ""),
    }
}


# Parse database configuration from $DATABASE_URL
DATABASES["default"] = dj_database_url.config()
SITE_ID = 1

# Set the variable true if running in docker environment
DOCKERIZED = int(os.environ.get("DOCKERIZED", 0)) == 1

USE_MINIO = int(os.environ.get("USE_MINIO", 0)) == 1

FILE_SIZE_LIMIT = int(os.environ.get("FILE_SIZE_LIMIT", 5242880))

# Enable Connection Pooling (if desired)
# DATABASES['default']['ENGINE'] = 'django_postgrespool'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# TODO: Make it FALSE and LIST DOMAINS IN FULL PROD.
CORS_ALLOW_ALL_ORIGINS = True


CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS += ("scout_apm.django",)

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Enable Connection Pooling (if desired)
# DATABASES['default']['ENGINE'] = 'django_postgrespool'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Allow all host headers
ALLOWED_HOSTS = [
    "*",
]


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


REDIS_URL = os.environ.get("REDIS_URL")

WEB_URL = os.environ.get("WEB_URL", "https://app.apencil.so")

LOGGER_BASE_URL = os.environ.get("LOGGER_BASE_URL", False)

redis_url = os.environ.get("REDIS_URL")
broker_url = (
    f"{redis_url}?ssl_cert_reqs={ssl.CERT_NONE.name}&ssl_ca_certs={certifi.where()}"
)


ENABLE_SIGNUP = os.environ.get("ENABLE_SIGNUP", "1") == "1"
