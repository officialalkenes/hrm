from django.urls import path

from . import views

app_name = "hotel"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("contact/", views.contact, name="contact-us"),
    path("events/", views.events, name="events"),
    path("all-rooms", views.all_rooms, name="all-rooms"),
    path("available-rooms/<rooms>/", views.available_rooms, name="available-rooms"),
    path("room-detail/<slug>/", views.room_detail, name="room-detail"),
    path("create-room/", views.create_room, name="create-room"),
    path("book-room/<slug>/", views.book_room, name="book-room"),
    path("dashboard/", views.hotel_dashboard, name="dashboard"),
]
