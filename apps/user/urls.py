from django.urls import path
from django.contrib.auth import views as views
# from django.contrib.auth.decorators import user_passes_test
from django.views.generic import TemplateView
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from .forms import PwdChangeForm, PwdResetForm, PwdResetConfirmForm

from . import views as view

app_name = "accounts"


urlpatterns = [
    path("signup/", view.signup_page, name="signup"),
    # path("<str:code>/", referral_view, name="ref-view"),
    # path("<pk>/profile-updating/", views.user_update, name="profile-updating"),
    # path("<pk>/wallet-updating/", wallet_update, name="wallet-updating"),
    path(
        "activate/<slug:uidb64>/<slug:token>/",
        view.activate_account_page,
        name="activate",
    ),
    path("login/", view.my_login_page, name="login"),
    path("logout/", view.logout_view, name="logout"),
    path(
        "reset-password/",
        PasswordResetView.as_view(template_name="users/password-reset.html"),
        name="reset_password",
    ),
    # path('login', views.LoginView.as_view(template_name='user/login.html'),
    #      name='login'),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(template_name="users/password_reset_sent.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_complete",
    ),
    path("password/", view.change_password, name="change_password"),
    # path('profile/<id>/edit/', update_profile, name='update-profile'),
    #     path('profile/<id>/kyc/', update_kyc, name='update-kyc'),
    path("delete/", view.delete_user, name="deactivate"),
]
