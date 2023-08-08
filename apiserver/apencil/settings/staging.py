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
DEBUG = int(os.environ.get("DEBUG", 1)) == 1
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("PGUSER", "plane"),
        "USER": "",
        "PASSWORD": "",
        "HOST": os.environ.get("PGHOST", "localhost"),
    }
}

# CORS WHITELIST ON PROD
CORS_ORIGIN_WHITELIST = [
    # "https://example.com",
    # "https://sub.example.com",
    # "http://localhost:8080",
    # "http://127.0.0.1:9000"
]
# Parse database configuration from $DATABASE_URL
DATABASES["default"] = dj_database_url.config()
SITE_ID = 1

# Enable Connection Pooling (if desired)
# DATABASES['default']['ENGINE'] = 'django_postgrespool'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Allow all host headers
ALLOWED_HOSTS = ["*"]

# TODO: Make it FALSE and LIST DOMAINS IN FULL PROD.
CORS_ALLOW_ALL_ORIGINS = True

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# Make true if running in a docker environment
DOCKERIZED = int(os.environ.get("DOCKERIZED", 0)) == 1
FILE_SIZE_LIMIT = int(os.environ.get("FILE_SIZE_LIMIT", 5242880))
USE_MINIO = int(os.environ.get("USE_MINIO", 0)) == 1

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[DjangoIntegration(), RedisIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    traces_sample_rate=1,
    send_default_pii=True,
    environment="staging",
    profiles_sample_rate=1.0,
)

STORAGES["default"] = {
        "BACKEND": "django_s3_storage.storage.S3Storage",
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

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"ssl_cert_reqs": False},
        },
    }
}

RQ_QUEUES = {
    "default": {
        "USE_REDIS_CACHE": "default",
    }
}


WEB_URL = os.environ.get("WEB_URL")

PROXY_BASE_URL = os.environ.get("PROXY_BASE_URL", False)

LOGGER_BASE_URL = os.environ.get("LOGGER_BASE_URL", False)

redis_url = os.environ.get("REDIS_URL")
broker_url = (
    f"{redis_url}?ssl_cert_reqs={ssl.CERT_NONE.name}&ssl_ca_certs={certifi.where()}"
)

ENABLE_SIGNUP = os.environ.get("ENABLE_SIGNUP", "1") == "1"