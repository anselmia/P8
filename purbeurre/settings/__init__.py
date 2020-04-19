"""
Django settings for purbeurre project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

#

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sentry_sdk.init(
    dsn="https://4498abeb937f4dc2a38222e458ba61f5@o379406.ingest.sentry.io/5204212",
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "uojp%c%-@l$aj0qc(v7(h3v63001h8$n=3g$7^g0j!)w-$#)r0"

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ["192.168.116.128", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    "substitute.apps.SubstituteConfig",
    "account.apps.AccountConfig",
    "home.apps.HomeConfig",
    "widget_tweaks",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "raven.contrib.django.raven_compat",
    "django_crontab",
]

RAVEN_CONFIG = {
    "dsn": "https://4498abeb937f4dc2a38222e458ba61f5@o379406.ingest.sentry.io/5204212",
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {"level": "WARNING", "handlers": ["sentry"],},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "sentry": {
            "level": "ERROR",  # To capture more than ERROR, change to WARNING, INFO, etc.
            "class": "raven.contrib.django.raven_compat.handlers.SentryHandler",
            "tags": {"custom-tag": "x"},
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "raven": {"level": "DEBUG", "handlers": ["console"], "propagate": False,},
        "sentry.errors": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware",
    "raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware",
]

ROOT_URLCONF = "purbeurre.urls"

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

WSGI_APPLICATION = "purbeurre.wsgi.application"

CRONJOBS = [("59 23 * * 3", "home.commands.update_db.update_product")]
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",  # on utilise l'adaptateur postgresql
#         "NAME": "purbeurre",  # le nom de notre base de donnees creee precedemment
#         "USER": "postgres",  # attention : remplacez par votre nom d'utilisateur
#         "PASSWORD": "arnaud06",
#         "HOST": "",
#         "PORT": "5432",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # on utilise l'adaptateur postgresql
        "NAME": "ocpizza",  # le nom de notre base de donnees creee precedemment
        "USER": "aanselmi",  # attention : remplacez par votre nom d'utilisateur
        "PASSWORD": "arnaud",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

AUTH_USER_MODEL = "account.User"

LOGIN_URL = "account:login"

LOGIN_REDIRECT_URL = "home:index"

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

CRISPY_TEMPLATE_PACK = "bootstrap4"

LANGUAGE_CODE = "fr-FR"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"

INTERNAL_IPS = ["127.0.0.1"]

DEBUG = True
