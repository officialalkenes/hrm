from django.urls import path

from . import views

app_name = "hotel"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("contact/", views.contact, name="contact-us"),
    path("events/", views.events, name="events"),
    path("all-rooms", views.all_rooms, name="all-rooms"),
    path("room-detail/<slug>/", views.room_detail, name="room-detail"),
    path("create-room/", views.CreateRoom.as_view(), name="create-room"),
]
