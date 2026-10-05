import os
from pathlib import Path

import cloudinary
import cloudinary.api
import cloudinary.uploader
from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent


APP_BASE_PATH = os.getenv("BASE_PATH", "").rstrip("/")
#FORCE_SCRIPT_NAME = APP_BASE_PATH or None
#STATIC_URL = f"{APP_BASE_PATH}/static/"
#MEDIA_URL = f"{APP_BASE_PATH}/media/"

FORCE_SCRIPT_NAME = "/erp"

# Asegúrate de que los archivos estáticos y de media también lo usen
STATIC_URL = "/erp/static/"
MEDIA_URL = "/erp/media/"

DEFENDER_REDIS_URL = os.getenv("DEFENDER_REDIS_URL")

# -----------------------------------------------------------------------------
# Core
# -----------------------------------------------------------------------------

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-wv*cx)e+oz3^zm029w!)x3v(-^xxzcuj^78b6*k-2_4%1ca10i",
)

DEBUG = True

ALLOWED_HOSTS = ["*"]


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
    #"zxcvbn_password",

    "ckeditor",
    "ckeditor_uploader",
]


LOCAL_APPS = [
    # Current project
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

    # django-allauth
    "allauth.account.middleware.AccountMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # OTP
    "django_otp.middleware.OTPMiddleware",

    # Custom ERP middleware
    "core.middleware.requests.RequestMiddleware",
    #"core.middleware.auth.CurrentUserMiddleware",
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
                #"expense.context_processors.get_total_expsense",
                #"expense.context_processors.get_total_expsense_by_month",
                #"expense.context_processors.get_total_expsense_by_year",
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

# Solo debe existir UN modelo de usuario.
AUTH_USER_MODEL = "authenticator.User"


LOGIN_REDIRECT_URL = "/dashboard"
LOGIN_URL = "/auth/sign-in/"
LOGOUT_REDIRECT_URL = "/"


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

TIME_ZONE = "UTC"

USE_I18N = True
USE_TZ = True


# -----------------------------------------------------------------------------
# Static files
# -----------------------------------------------------------------------------

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# -----------------------------------------------------------------------------
# Media
# -----------------------------------------------------------------------------

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# -----------------------------------------------------------------------------
# CKEditor
# -----------------------------------------------------------------------------

CKEDITOR_BASEPATH = "/static/ckeditor/"

CKEDITOR_UPLOAD_PATH = "uploads/"


# -----------------------------------------------------------------------------
# Crispy Forms
# -----------------------------------------------------------------------------

CRISPY_TEMPLATE_PACK = "bootstrap4"


# -----------------------------------------------------------------------------
# Phone Numbers
# -----------------------------------------------------------------------------

PHONENUMBER_DEFAULT_REGION = "BD"


# -----------------------------------------------------------------------------
# Formatting
# -----------------------------------------------------------------------------

USE_THOUSAND_SEPARATOR = True

THOUSAND_SEPARATOR = ","


# -----------------------------------------------------------------------------
# Email
# -----------------------------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# -----------------------------------------------------------------------------
# Cache
# -----------------------------------------------------------------------------

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": BASE_DIR / "cache",
    }
}