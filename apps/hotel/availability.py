import datetime

from .models import Room, Booking


def check_availability(room, checkin, checkout):
    available_list = []
    bookings = Booking.objects.filter(room=room)

    for booking in bookings:
        if booking.check_in > checkout or booking.check_out < checkin:
            available_list.append(True)
        available_list.append(False)
    print(all(available_list))
    return all(available_list)
