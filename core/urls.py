from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.user.urls", namespace="accounts")),
    path("", include("apps.hotel.urls", namespace="hotel")),
    path("invoice/", include("apps.invoice.urls", namespace="invoice")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
