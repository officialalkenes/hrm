from django.shortcuts import get_object_or_404, redirect, render

from django.urls import reverse_lazy

from django.views.generic import (
    CreateView,
    FormView,
    ListView,
    UpdateView,
    DetailView,
    View,
)
from apps.hotel.availability import check_availability

from apps.hotel.forms import AvailabilityForm, EventForm, RoomForm, RoomImageFormset

from .models import Event, Room, Booking, RoomType


def test(request):
    return render(request, "hotel/index.html")


def homepage(request):
    specials = Room.objects.all()[:5]
    room_cats = RoomType.objects.all()
    context = {
        "specials": specials,
        "room_cats": room_cats,
    }
    return render(request, "hotel/home.html", context)


def events(request):
    events = Event.objects.all()
    context = {
        "events": events,
    }
    return render(request, "events.html", context)


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


def room_categories(request):
    room_cat = RoomType.objects.all()
    context = {"cats": room_cat}
    return render(request, "", context)


def category_details(request, slug):
    try:
        room_cat = RoomType.objects.filter(slug=slug).first()
    except RoomType.DoesNotExist:
        pass
    rooms = Room.objects.filter(room_type=room_cat)
    available_rooms = []
    booked_rooms = []
    for room in rooms:
        if check_availability(room, room.checkin, room.checkout):
            available_rooms.append(room)
        else:
            booked_rooms.append(room)
    context = {
        "available_rooms": available_rooms,
        "booked_rooms": booked_rooms,
    }
    return render(request, "", context)


# class CategoryDetailView(View):
#     def get(self, request, *args, **kwargs):
#         category = self.kwargs.get('slug', None)
#         form = AvailabilityForm()
#         rooms = Room.objects.filter(category=category)
#         if len(rooms) > 0:
#             room_category = rooms[0].room_type.name
#             context = {
#                 'category': room_category,
#                 'form': form}
#             return render(request, '', context)
#         return redirect("cat-error")

#     def post(self, request, *args, **kwargs):
#         category = self.kwargs.get('slug', None)
#         rooms = Room.objects.filter(category=category)
#         rooms_available = []
#         for room in rooms:
#             ...


class BookingRoomView(FormView):
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


class BookingEventView(FormView):
    form_class = EventForm
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


class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm
    success_url = reverse_lazy("products")
    template_name = ""

    def get_context_data(self, **kwargs):
        context = super(RoomCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = RoomImageFormset(self.request.POST, self.request.FILES)
        else:
            context["formset"] = RoomImageFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.user = self.request.user
        formset = context["formset"]
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super(RoomCreateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


create_room = RoomCreateView.as_view()


class UpdateRoomView(UpdateView):
    model = Room
    form_class = RoomForm
    template_name = ".html"
    success_url = reverse_lazy("my_model_list")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        inline_formset = RoomImageFormset(instance=self.object)
        return self.render_to_response(
            self.get_context_data(form=form, inline_formset=inline_formset)
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        inline_formset = RoomImageFormset(request.POST, instance=self.object)
        if form.is_valid() and inline_formset.is_valid():
            return self.form_valid(form, inline_formset)
        else:
            return self.form_invalid(form, inline_formset)

    def form_valid(self, form, inline_formset):
        self.object = form.save()
        inline_formset.save()
        return super().form_valid(form)

    def form_invalid(self, form, inline_formset):
        return self.render_to_response(
            self.get_context_data(form=form, inline_formset=inline_formset)
        )
