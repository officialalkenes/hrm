from django.shortcuts import render

from .models import Room, Booking


def homepage(request):
    rooms = Room.objects.all()[:5]
    context = {
        "rooms": rooms,
    }
    return render(request, "", context)
