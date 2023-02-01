from django.shortcuts import get_object_or_404, redirect, render

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

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

from apps.hotel.availability import availability_checker, check_availability

from apps.hotel.forms import (
    AvailabilityForm,
    BookingForm,
    ContactForm,
    EventForm,
    RoomAvailabilityForm,
    RoomDetailAvailabilityForm,
    RoomForm,
)
from apps.hotel.utils import send_contact_email

from .models import Event, Room, Booking, RoomType

User = get_user_model()


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
        form = RoomAvailabilityForm(request.POST)
        if form.is_valid():
            guest = form.cleaned_data.get("people")
            beds = form.cleaned_data.get("beds")
            checkin = form.cleaned_data.get("check_in")
            checkout = form.cleaned_data.get("check_out")
            all_rooms = Room.objects.filter(capacity__gte=guest, beds__gte=beds)
            available_rooms = []
            for room in all_rooms:
                if availability_checker(room, checkin, checkout):
                    available_rooms.append(room)
            return render(
                request, "hotel/available-rooms.html", {"rooms": available_rooms}
            )
    context = {"specials": specials, "room_cats": room_cats, "form": form}
    return render(request, "hotel/index.html", context)


def available_rooms(request, rooms):
    available = Room.objects.filter(is_available=True)
    context = {"available": available}
    return render(request, "hotel/available-rooms.html", context)


def dashboard(request):
    # rooms = Room.objects.all()

    context = {}
    return render(request, "", context)


def events(request):
    events = Event.objects.all()
    context = {
        "events": events,
    }
    return render(request, "hotel/events.html", context)


def all_rooms(request):
    rooms = Room.objects.all()
    paginator = Paginator(rooms, 6)
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
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "New Room Created Successfully.")
            return redirect("")
    context = {
        "form": form,
    }
    return render(request, "dashboard/", context)


def update_room(request, slug):
    room = get_object_or_404(Room, slug=slug)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("success_url")
    else:
        form = RoomForm(instance=room)
    return render(request, "update_template.html", {"form": form})


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
    template_name = "hotel/booking.html"

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


def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("hotel:homepage")
    context = {"form": form}
    return render(request, "dashboard/create-room.html", context)


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


# views.py
def book_room(request, slug):
    room = Room.objects.get(slug=slug)
    form = BookingForm()
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            checkin = form.cleaned_data["check_in"]
            checkout = form.cleaned_data["check_out"]
            if availability_checker(room, checkin, checkout):
                booking = form.save(commit=False)
                booking.room = room
                booking.customer = request.user
                booking.save()
                room.is_available = False
                room.save()
                context = {
                    "booking": booking,
                    "paystack_public_key": settings.PAYSTACK_PUBLIC_KEY,
                }
                messages.success(request, "Room has been Booked Successfully.")
                return render(request, "hotel/initiate_payment.html", context)
            else:
                messages.error(
                    request, "Sorry! Room has already been booked for selected date."
                )
                return redirect("hotel:book-room", slug)
    return render(request, "hotel/book_room.html", {"room": room, "form": form})


def hotel_dashboard(request):
    hotels = Room.objects.all()
    bookings = Booking.objects.all()
    users = User.objects.all()
    rooms_available = []
    for room in hotels:
        if availability_checker(room):
            rooms_available.append(room)
    context = {
        "hotels": hotels,
        "bookings": bookings,
        "users": users,
        "rooms_available": rooms_available,
        "visitors": len(users),
    }
    return render(request, "hotel/dashboard.html", context)


def guest_list(request):
    context = {}
    return render(request, "", context)


def guest_detail(request, ref):
    context = {}
    return render(request, "", context)
