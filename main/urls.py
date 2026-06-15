from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    
    # Custom Auth URLs to ensure they use our templates and not Django Admin defaults
    path("accounts/login/", auth_views.LoginView.as_view(template_name="main/auth/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    # Custom 6-digit code password reset
    path("accounts/password_reset/", views.custom_password_reset, name="password_reset"),
    path("accounts/password_reset/verify/", views.custom_password_reset_verify, name="password_reset_verify"),
    path("accounts/password_reset/confirm/", views.custom_password_reset_confirm, name="password_reset_confirm_custom"),
    path("accounts/password_reset/complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name="main/auth/password_reset_complete.html"
    ), name="password_reset_complete_custom"),
    
    path("accounts/register/", views.register, name="register"),
    path("accounts/profile/", views.profile, name="profile"),
    path("mod/<int:mod_id>/", views.mod_detail, name="mod_detail"),
    path("category/<int:category_id>/", views.category_detail, name="category_detail"),
    path("cart/", views.view_cart, name="view_cart"),
    path("cart/add/<int:mod_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:mod_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("subscribe/", views.subscribe_newsletter, name="subscribe_newsletter"),
    ]