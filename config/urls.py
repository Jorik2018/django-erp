# flake8: noqa

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


# -----------------------------------------------------------------------------
# Django Admin
# -----------------------------------------------------------------------------

admin.site.site_header = "Django ERP"
admin.site.site_title = "Django ERP"
admin.site.index_title = "Django ERP Administration"


# -----------------------------------------------------------------------------
# URLs
# -----------------------------------------------------------------------------

urlpatterns = [
    # -------------------------------------------------------------------------
    # Dashboard
    # -------------------------------------------------------------------------

    path("", include("core.urls")),

    # Legacy pages
    path("pages/", include("pages.urls")),

    # -------------------------------------------------------------------------
    # REST API
    # -------------------------------------------------------------------------

    path(
        "api/",
        include("people.api.urls"),
    ),

    path(
        "api/auth/",
        include("auth_arena.urls"),
    ),

    path(
        "api/study/",
        include("study_arena.urls"),
    ),

    # -------------------------------------------------------------------------
    # ERP
    # -------------------------------------------------------------------------

    path(
        "customers/",
        include("customers.urls"),
    ),

    path(
        "profile/",
        include("profiles.urls"),
    ),

    path(
        "purchase/",
        include("purchase.urls"),
    ),

    path(
        "products/",
        include("products.urls"),
    ),

    path(
        "service/",
        include("service.urls"),
    ),

    path(
        "suppliers/",
        include("suppliers.urls"),
    ),

    path(
        "settings/",
        include("settings.urls"),
    ),

    path(
        "sales/",
        include("sales.urls"),
    ),

    path(
        "order/",
        include("order.urls"),
    ),

    path(
        "expense/",
        include("expense.urls"),
    ),

    path(
        "return/",
        include("returns.urls"),
    ),

    path(
        "damage/",
        include("damage.urls"),
    ),

    path(
        "stock/",
        include("stock.urls"),
    ),

    path(
        "accounts/",
        include("accounts.urls"),
    ),

    path(
        "analytics/",
        include("analytics.urls"),
    ),

    # -------------------------------------------------------------------------
    # Authentication
    # -------------------------------------------------------------------------

    path(
        "accounts-user/",
        include("allauth.urls"),
    ),

    path(
        "auth/",
        include("authenticator.urls"),
    ),

    # -------------------------------------------------------------------------
    # Admin
    # -------------------------------------------------------------------------

    path(
        "admin/",
        admin.site.urls,
    ),

    # -------------------------------------------------------------------------
    # Defender
    # -------------------------------------------------------------------------

    path(
        "admin/defender/",
        include("defender.urls"),
    ),
]


# -----------------------------------------------------------------------------
# Development Media
# -----------------------------------------------------------------------------

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )