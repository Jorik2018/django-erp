from django.urls import path

from profiles.views.account_data_views import account_data
from settings.views.delete_account_views import DeleteAccountView
from settings.views.login_activity_views import LoginActivityView
from settings.views.password_change_views import passwordChangeView
from settings.views.price_plans_views import PricePlansView
from settings.views.privacy_and_security_views import PrivacyAndSecurityView
from settings.views.settings_views import settings


urlpatterns = [
    path("", settings, name="settings"),
    path("plans/", PricePlansView.as_view(), name="price_plans"),

    path(
        "password/change/",
        passwordChangeView,
        name="password_change",
    ),

    path(
        "accounts/privacy_and_security/",
        PrivacyAndSecurityView.as_view(),
        name="privacy_and_security",
    ),

    path(
        "accounts/delete/",
        DeleteAccountView.as_view(),
        name="delete_account",
    ),

    path(
        "accounts/data/",
        account_data,
        name="account_data",
    ),

    path(
        "login-activity/",
        LoginActivityView.as_view(),
        name="login_activity",
    ),
]