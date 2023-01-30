from django.urls import path

from . import views

app_name = "invoice"

urlpatterns = [
    path("initiate-payment/", views.initiate_payment, name="initiate-payment")
]
