from django.urls import include, path

from cryptotracker.form import AccountForm, EditUserAddressForm
from cryptotracker.models import Account, UserAddress
from cryptotracker.views import (
    accounts,
    address_detail,
    check_task_status,
    delete_object,
    edit_object,
    home,
    portfolio,
    refresh,
    sign_up,
    staking,
    statistics,
    user_addresses,
    waiting_page,
    rewards,
    admin_panel,
    generate_invite_code,
    invite_codes,
    revoke_invite_code,
    user_management,
    toggle_admin_status,
)

urlpatterns = [
    path("", home, name="home"),
    path("accounts/", accounts, name="accounts"),
    path("portfolio/", portfolio, name="portfolio"),
    path("portfolio/<str:date_str>/", portfolio, name="portfolio_with_date"),
    path("user_addresses/", user_addresses, name="user_addresses"),
    path("user_address/<str:public_address>/", address_detail, name="address_detail"),
    path("user_addresses/", include("django.contrib.auth.urls")),
    path("sign_up/", sign_up, name="sign_up"),
    path(
        "user_address/<str:id>/delete/",
        delete_object,
        {
            "model": UserAddress,
            "redirect_url": "user_addresses",
            "object_type": "UserAddress",
        },
        name="delete_address",
    ),
    path(
        "account/<str:id>/delete/",
        delete_object,
        {"model": Account, "redirect_url": "accounts", "object_type": "Account"},
        name="delete_account",
    ),
    path("refresh/", refresh, name="refresh"),
    path("staking/", staking, name="staking"),
    path(
        "user_address/<str:id>/edit/",
        edit_object,
        {
            "model": UserAddress,
            "redirect_url": "user_addresses",
            "form": EditUserAddressForm,
            "object_type": "UserAddress",
        },
        name="edit_address",
    ),
    path(
        "account/<str:id>/edit/",
        edit_object,
        {
            "model": Account,
            "redirect_url": "accounts",
            "form": AccountForm,
            "object_type": "Account",
        },
        name="edit_account",
    ),
    path("waiting_page/", waiting_page, name="waiting_page"),
    path("check_task_status/", check_task_status, name="check_task_status"),
    path("statistics/", statistics, name="statistics"),
    path("rewards/", rewards, name="rewards"),
    # Admin URLs
    path("admin/", admin_panel, name="admin_panel"),
    path("admin/generate_invite_code/", generate_invite_code, name="generate_invite_code"),
    path("admin/invite_codes/", invite_codes, name="invite_codes"),
    path("admin/revoke_invite_code/<int:code_id>/", revoke_invite_code, name="revoke_invite_code"),
    path("admin/user_management/", user_management, name="user_management"),
    path("admin/toggle_admin/<int:user_id>/", toggle_admin_status, name="toggle_admin"),
]
