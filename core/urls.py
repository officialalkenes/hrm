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


admin.site.site_header = "FreshKom4t Admin"
admin.site.index_title = "Welcome To FreshKom4t Admin Portal"
admin.site.site_title = "FreshKom4t Admin Portal"

handler404 = "apps.user.views.handler404"
handler500 = "apps.user.views.handle_server_error"
