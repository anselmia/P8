import dj_database_url
import os

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = True
# Static files settings
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(PROJECT_ROOT, "staticfiles")

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "static"),)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

db_from_env = dj_database_url.config(conn_max_age=500)

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

DATABASES["default"].update(db_from_env)
