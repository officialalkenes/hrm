from django.conf import settings
from django.contrib.auth.decorators import user_passes_test


def superuser_required(function=None):
    """
    Decorator for views that checks that the user is a superuser,
    redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser, login_url=settings.LOGIN_URL, redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def active_staff_required(function=None):
    """
    Decorator for views that checks that the user is a superuser,
    redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_staff and u.is_active,
        login_url=settings.LOGIN_URL,
        redirect_field_name=None,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
