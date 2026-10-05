import os
from pathlib import Path

import cloudinary
import cloudinary.api
import cloudinary.uploader
from dotenv import load_dotenv


load_dotenv()


# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


# -----------------------------------------------------------------------------
# Base path
# -----------------------------------------------------------------------------

APP_BASE_PATH = os.getenv("BASE_PATH", "").rstrip("/")

FORCE_SCRIPT_NAME = APP_BASE_PATH or None

STATIC_URL = f"{APP_BASE_PATH}/static/"
MEDIA_URL = f"{APP_BASE_PATH}/media/"


# -----------------------------------------------------------------------------
# Core
# -----------------------------------------------------------------------------

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-wv*cx)e+oz3^zm029w!)x3v(-^xxzcuj^78b6*k-2_4%1ca10i",
)

DEBUG = os.getenv("DEBUG", "true").lower() == "true"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "*",
).split(",")


# -----------------------------------------------------------------------------
# Redis / Defender
# -----------------------------------------------------------------------------

DEFENDER_REDIS_URL = os.getenv("DEFENDER_REDIS_URL")


# -----------------------------------------------------------------------------
# Cloudinary
# -----------------------------------------------------------------------------

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
)


# -----------------------------------------------------------------------------
# Applications
# -----------------------------------------------------------------------------

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
]


THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",

    "import_export",
    "django_user_agents",
    "django_filters",

    "crispy_forms",
    "crispy_bootstrap4",

    "django_countries",
    "phonenumber_field",

    "allauth",
    "allauth.account",
    "allauth.socialaccount",

    "django_otp",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_static",

    "defender",

    "ckeditor",
    "ckeditor_uploader",
]


LOCAL_APPS = [
    # APIs / legacy modules
    "people.apps.PeopleConfig",
    "auth_arena.apps.AuthArenaConfig",
    "study_arena.apps.StudyArenaConfig",

    # ERP
    "core.apps.CoreConfig",
    "stock.apps.StockConfig",
    "expense.apps.ExpenseConfig",
    "sales.apps.SalesConfig",
    "service.apps.ServiceConfig",
    "returns.apps.ReturnsConfig",
    "damage.apps.DamageConfig",
    "settings.apps.SettingsConfig",
    "profiles.apps.ProfilesConfig",
    "products.apps.ProductsConfig",
    "accounts.apps.AccountsConfig",
    "purchase.apps.PurchaseConfig",
    "suppliers.apps.SuppliersConfig",
    "customers.apps.CustomersConfig",
    "authenticator.apps.AuthenticatorConfig",
    "analytics.apps.AnalyticsConfig",
    "order.apps.OrderConfig",
    "report.apps.ReportConfig",
]


INSTALLED_APPS = (
    DJANGO_APPS
    + THIRD_PARTY_APPS
    + LOCAL_APPS
)


SITE_ID = 1

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# -----------------------------------------------------------------------------
# Middleware
# -----------------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.gzip.GZipMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "allauth.account.middleware.AccountMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "django_otp.middleware.OTPMiddleware",

    # Custom ERP
    "core.middleware.requests.RequestMiddleware",

    # Dejamos este deshabilitado por el problema que vimos
    # con respuestas 403 globales.
    # "core.middleware.auth.CurrentUserMiddleware",
]


ROOT_URLCONF = "config.urls"


# -----------------------------------------------------------------------------
# Templates
# -----------------------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                # Expense
                "expense.context_processors.expense_totals",

                # Customers
                "customers.context_processors.customer_created_at_january",
                "customers.context_processors.customer_created_at_february",
                "customers.context_processors.customer_created_at_march",
                "customers.context_processors.customer_created_at_april",
                "customers.context_processors.customer_created_at_may",
                "customers.context_processors.customer_created_at_june",
                "customers.context_processors.customer_created_at_july",
                "customers.context_processors.customer_created_at_august",
                "customers.context_processors.customer_created_at_september",
                "customers.context_processors.customer_created_at_october",
                "customers.context_processors.customer_created_at_november",
                "customers.context_processors.customer_created_at_december",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"


# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# -----------------------------------------------------------------------------
# Authentication
# -----------------------------------------------------------------------------

AUTH_USER_MODEL = "authenticator.User"


LOGIN_URL = "sign-in"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "sign-in"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# -----------------------------------------------------------------------------
# Django REST Framework
# -----------------------------------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
}


# -----------------------------------------------------------------------------
# Internationalization
# -----------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = os.getenv(
    "TIME_ZONE",
    "America/Lima",
)

USE_I18N = True
USE_TZ = True


# -----------------------------------------------------------------------------
# Static files
# -----------------------------------------------------------------------------

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# -----------------------------------------------------------------------------
# Media
# -----------------------------------------------------------------------------

MEDIA_ROOT = BASE_DIR / "media"


# -----------------------------------------------------------------------------
# CKEditor
# -----------------------------------------------------------------------------

CKEDITOR_BASEPATH = f"{APP_BASE_PATH}/static/ckeditor/"

CKEDITOR_UPLOAD_PATH = "uploads/"


# -----------------------------------------------------------------------------
# Crispy Forms
# -----------------------------------------------------------------------------

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"


# -----------------------------------------------------------------------------
# Phone Numbers
# -----------------------------------------------------------------------------

PHONENUMBER_DEFAULT_REGION = os.getenv(
    "PHONENUMBER_DEFAULT_REGION",
    "PE",
)


# -----------------------------------------------------------------------------
# Formatting
# -----------------------------------------------------------------------------

USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ","


# -----------------------------------------------------------------------------
# Email
# -----------------------------------------------------------------------------

EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
)


# -----------------------------------------------------------------------------
# Cache
# -----------------------------------------------------------------------------

CACHES = {
    "default": {
        "BACKEND": (
            "django.core.cache.backends.filebased."
            "FileBasedCache"
        ),
        "LOCATION": BASE_DIR / "cache",
    }
}

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CSRF_TRUSTED_ORIGINS",
        "",
    ).split(",")
    if origin.strip()
]

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)