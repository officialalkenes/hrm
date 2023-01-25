from django.urls import path

from . import views

app_name = "hotel"

urlpatterns = [
    path("", views.all_rooms, "rooms"),
    path("contact/", views.contact, "contact-us"),
    path("events/", views.events, "events"),
    path("room-detail/<slug>/", views.room_detail, "room-detail"),
]
