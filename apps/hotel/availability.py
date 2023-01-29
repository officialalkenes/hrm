import datetime
from django.db.models import Q


# from apps.invoice.models import Hall

from .models import Room, Booking


def availability_checker(room, checkin, checkout):
    bookings = Booking.objects.filter(room=room)
    unavailable_bookings = bookings.filter(
        Q(check_in__gte=checkin, check_in__lt=checkout)
        | Q(check_out__gt=checkin, check_out__lte=checkout)
    )
    return not unavailable_bookings.exists()


def check_availability(room, checkin, checkout):
    available_list = []
    bookings = Booking.objects.filter(room=room)

    for booking in bookings:
        if booking.check_in < checkout and booking.check_out < checkin:
            available_list.append(True)
        available_list.append(False)
    return all(available_list)


# def check_hall_availability(checkin, checkout):
#     available_list = []
#     # hall_record = HallBooking.objects.all()

#     for hall in hall_record:
#         if hall.check_in > checkout or hall.check_out < checkin:
#             available_list.append(True)
#     return all(available_list)
