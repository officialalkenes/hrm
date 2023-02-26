from django.urls import path

from . import views

app_name = "hotel"

urlpatterns = [
    # Normal View
    path("", views.homepage, name="homepage"),
    path("contact/", views.contact, name="contact-us"),
    path("events/", views.events, name="events"),
    path("all-rooms", views.all_rooms, name="all-rooms"),
    path("available-rooms/<rooms>/", views.available_rooms, name="available-rooms"),
    path("room-detail/<slug>/", views.room_detail, name="room-detail"),
    path("create-room/", views.create_room, name="create-room"),
    path("book-room/<slug>/", views.book_room, name="book-room"),
    path("book-pay-room/<slug>/", views.book_and_pay_room, name="book-pay-room"),
    path("payment-records/", views.payment_records, name="payment-records"),
    path("booking-list/", views.check_bookings, name="booking-list"),
    # Admin View
    path("dashboard/", views.hotel_dashboard, name="dashboard"),
    path("contacts/", views.contact_list, name="contacts"),
    path("guest-list/", views.guest_list, name="guest-list"),
    path("room-type/", views.add_new_roomtype, name="room-type"),
    path("add-staff/", views.add_new_staff, name="add-staff"),
    path("staff-list/", views.staff_list, name="staff-list"),
    path(
        "admin-payment-records/",
        views.admin_payment_records,
        name="admin-payment-records",
    ),
    path("admin-add-payment/", views.admin_payment, name="admin-add-payment"),
    path("update-booking/<ref>/", views.update_booking, name="update-booking"),
    path("update-payment/<ref>/", views.update_payment, name="update-payment"),
    path("guest-detail/<ref>/", views.guest_detail, name="guest-detail"),
]
