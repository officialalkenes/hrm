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
    path("book-pay-room/<slug>/", views.book_and_pay_room, name="book-pay-room"),
    path("dashboard/", views.hotel_dashboard, name="dashboard"),
    path("guest-list/", views.guest_list, name="guest-list"),
    path("booking-list/", views.check_bookings, name="booking-list"),
    path("payment-records/", views.payment_records, name="payment-records"),
    path(
        "admin-payment-records/",
        views.admin_payment_records,
        name="admin-payment-records",
    ),
    path("update-booking/<ref>/", views.update_booking, name="update-booking"),
    path("guest-detail/<ref>/", views.guest_detail, name="guest-detail"),
]
