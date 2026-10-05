# flake8: noqa

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Opcional: si instalas django-otp
# from django_otp.admin import OTPAdminSite

# Opcional: habilitar 2FA solo en producción
#
# if not settings.DEBUG:
#     admin.site.__class__ = OTPAdminSite


admin.site.site_header = "Django ERP"
admin.site.site_title = "Django ERP"
admin.site.index_title = "Django ERP Administration"

admin.autodiscover()


urlpatterns = [
    path("", include("core.urls")),

    # Si todavía quieres conservar pages
    path("pages/", include("pages.urls")),
    
    # API REST
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

    # ERP modules
    path("customers/", include("customers.urls")),
    path("profile/", include("profiles.urls")),
    path("purchase/", include("purchase.urls")),
    path("products/", include("products.urls")),
    path("service/", include("service.urls")),
    path("suppliers/", include("suppliers.urls")),
    path("settings/", include("settings.urls")),
    path("sales/", include("sales.urls")),
    path("order/", include("order.urls")),
    path("expense/", include("expense.urls")),
    path("return/", include("returns.urls")),
    path("damage/", include("damage.urls")),
    path("stock/", include("stock.urls")),
    path("accounts/", include("accounts.urls")),
    path("analytics/", include("analytics.urls")),

    # Authentication
    path("accounts-user/", include("allauth.urls")),
    path("auth/", include("authenticator.urls")),

    # Admin
    path("admin/", admin.site.urls),

    # Security / Defender
    path(
        "admin/defender/",
        include("defender.urls"),
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )