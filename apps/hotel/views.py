from django.shortcuts import get_object_or_404, redirect, render

from django.views.generic import CreateView, FormView, ListView, UpdateView, DetailView


from .models import Room, Booking


def homepage(request):
    specials = Room.objects.all()[:5]
    context = {
        "specials": specials,
    }
    return render(request, "", context)


def all_rooms(request):
    rooms = Room.objects.all()
    context = {
        "rooms": rooms,
    }
    return render(request, "", context)


def room_detail(request, slug):
    try:
        room = get_object_or_404(Room, slug)
        types = room.room_type
    except Room.DoesNotExist:
        pass
    related_room = Room.objects.filter(room_type=types)[:4]
    context = {
        "room": room,
        "related_room": related_room,
    }
    return render(request, "", context)


class CreateRoom(CreateView):
    model = Room
    fields = ""
