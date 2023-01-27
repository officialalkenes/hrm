from django.shortcuts import get_object_or_404, redirect, render

from django.core.paginator import Paginator
from django.contrib import messages

from django.forms import inlineformset_factory

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

from apps.hotel.forms import (
    AvailabilityForm,
    ContactForm,
    EventForm,
    RoomAvailabilityForm,
    RoomDetailAvailabilityForm,
    RoomForm,
)
from apps.hotel.utils import send_contact_email

from .models import Event, Room, Booking, RoomType


def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            subject = form.cleaned_data.get("subject")
            name = form.cleaned_data.get("name")
            content = form.cleaned_data.get("message")
            send_contact_email(
                name, email, subject, content, "hotel/contact-email.html"
            )
            messages.success(request, "Thank you for your message. It has been sent.")
            form.save()
            return redirect("hotel:contact-us")
    context = {
        "form": form,
    }
    return render(request, "hotel/contact.html", context)


def homepage(request):
    specials = Room.objects.all()[:4]
    room_cats = RoomType.objects.all()
    form = RoomAvailabilityForm()
    if request.method == "POST":
        form = RoomDetailAvailabilityForm(request.POST)
        if form.is_valid():
            guest = form.cleaned_data.get("guest")
            capacity = form.cleaned_data.get("capacity")
            check_in = form.cleaned_data.get("check_in")
            check_out = form.cleaned_data.get("check_out")
            rooms = Room.objects.filter(guest=guest, capacity__gte=capacity)
            available_rooms = []
            for room in rooms:
                if check_availability(room, check_in, check_out):
                    available_rooms.append(room)
                return redirect("")
    context = {"specials": specials, "room_cats": room_cats, "form": form}
    return render(request, "hotel/index.html", context)


def events(request):
    events = Event.objects.all()
    context = {
        "events": events,
    }
    return render(request, "hotel/events.html", context)


def all_rooms(request):
    rooms = Room.objects.all()
    paginator = Paginator(rooms, 2)
    page_number = request.GET.get("page")
    page_number = page_number if page_number else 1
    try:
        current_page = paginator.page(page_number)
    except page_number.DoesNotExist:
        current_page = paginator.page(1)
    context = {"rooms": rooms, "page_obj": current_page}
    return render(request, "hotel/rooms.html", context)


def room_detail(request, slug):
    try:
        room = Room.objects.get(slug=slug)
        types = room.room_type
        # if check_availability(room, checkin, checkout):
        # availablity = True
        # availablity = False
    except Room.DoesNotExist:
        pass
    related_room = Room.objects.filter(room_type=types)[:4]
    context = {
        "room": room,
        "related_room": related_room,
    }
    return render(request, "hotel/room-detail.html", context)


def create_new_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New Room Created Successfully.")
            return redirect("")
    context = {
        "form": form,
    }
    return render(request, "", context)


class RoomDetailView(View):
    def get(self, request, slug):
        try:
            room = get_object_or_404(Room, self.slug)
            types = room.type
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

    def post(self, request, slug):
        room = Room.objects.get(slug=slug)
        form = RoomDetailAvailabilityForm()
        if request.method == "POST":
            form = RoomDetailAvailabilityForm(request.POST)
            if form.is_valid():
                checkin = form.get("check_in", None)
                checkout = form.get("check_out", None)
                if check_availability(room, checkin, checkout):
                    messages.success("Room is Available. You can book now")
                else:
                    messages.info("Room is Booked. Check back next time")
        context = {}
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
        # inline_formset = RoomImageFormset(instance=self.object)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # inline_formset = RoomImageFormset(request.POST, instance=self.object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, inline_formset):
        self.object = form.save()
        inline_formset.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
