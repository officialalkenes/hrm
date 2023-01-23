from django.shortcuts import get_object_or_404, redirect, render

from django.views.generic import CreateView, FormView, ListView, UpdateView, DetailView
from apps.hotel.availability import check_availability

from apps.hotel.forms import AvailabilityForm
from apps.hotel.utils import get_room

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
        # if check_availability(room, checkin, checkout):
        #     availablity = True
        # availablity = False
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


class BookingSelectionView(FormView):
    form_class = AvailabilityForm
    template_name = ""

    def form_valid(self, form):
        data = form.cleaned_data
        category = data["room_category"]
        room_list = Room.objects.filter(room_type=category)
        available_rooms = []
        checkin = data["check_in"]
        checkout = data["check_out"]
        for room in room_list:
            if check_availability(room, checkin, checkout):
                available_rooms.append(room)
        if len(available_rooms) == 0:
            return redirect("hotels:no-room-found")
        return super().form_valid(form)
