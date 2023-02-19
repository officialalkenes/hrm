from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator

from django.forms import inlineformset_factory

from django.utils import timezone
from django.urls import reverse_lazy, reverse

from django.views.generic import (
    CreateView,
    FormView,
    ListView,
    UpdateView,
    DetailView,
    View,
)

from apps.invoice.models import Payment

from .mixins import AdminRequiredMixin
from apps.hotel.availability import availability_checker, check_availability

from apps.hotel.forms import (
    AdminBookingForm,
    AdminPaymentForm,
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


def check_bookings(request):
    user = request.user
    bookings = Booking.objects.filter(customer=user)
    context = {
        "bookings": bookings,
    }
    return render(request, "dashboard/booking-list.html", context)


def payment_records(request):
    user = request.user
    payments = Payment.objects.filter(booking__customer=user)
    context = {
        "payments": payments,
    }
    return render(request, "dashboard/payment-record.html", context)


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


def room_detail(request, slug):
    room = Room.objects.get(slug=slug)
    if request.method == "POST":
        checkin = request.POST.get("checkin")
        checkout = request.POST.get("checkout")
        checkin_date = timezone.datetime.strptime(checkin, "%d %B, %Y").date()
        formatted_checkin = checkin_date.strftime("%Y-%m-%d")
        checkout_date = timezone.datetime.strptime(checkout, "%d %B, %Y").date()
        formatted_checkout = checkout_date.strftime("%Y-%m-%d")
        if availability_checker(room, formatted_checkin, formatted_checkout):
            messages.success(
                request,
                f"Room is Available between {checkin} and {checkout}. You can book now",
            )
            return redirect("hotel:room-detail", slug)
        else:
            messages.error(request, f"Room is Booked between {checkin} and {checkout}")
            return redirect("hotel:room-detail", slug)

    else:
        types = room.room_type
        # if check_availability(room, checkin, checkout):
        #     availablity = True
        # availablity = False
        related_room = Room.objects.filter(room_type=types)[:4]
        context = {
            "room": room,
            "related_room": related_room,
        }
        return render(request, "hotel/room-detail.html", context)


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


class BookingEventView(SuccessMessageMixin, FormView):
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


class UpdateRoomView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Room
    fields = [
        "amount",
        "payment",
    ]
    template_name = "dashboard/update-room.html"
    success_message = "Room has been updated successfully!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("investicon:deposit-records")


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
                messages.success(request, "Room has been Booked Successfully.")
                return redirect("hotel:book-room")
            else:
                messages.error(
                    request, "Sorry! Room has already been booked for selected date."
                )
                return redirect("hotel:book-room", slug)
    return render(request, "hotel/book_room.html", {"room": room, "form": form})


def book_and_pay_room(request, slug):
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
    rooms = Room.objects.all()
    bookings = Booking.objects.all()
    users = User.objects.all()
    rooms_available = rooms.filter(is_available=True)
    context = {
        "rooms": rooms,
        "bookings": bookings,
        "users": users,
        "rooms_available": rooms_available,
        "visitors": len(users),
    }
    return render(request, "dashboard/dashboard.html", context)


def guest_list(request):
    guests = Booking.objects.all()
    context = {
        "guests": guests,
    }
    return render(request, "dashboard/guest-list.html", context)


def update_booking(request, ref):
    booking = Booking.objects.get(reference_id=ref)
    if request.method == "POST":
        form = AdminBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect("hotel:guest-list")
    else:
        form = AdminBookingForm(instance=booking)
    return render(request, "dashboard/create-booking.html", {"form": form})


def admin_booking(request):
    form = AdminBookingForm()
    if request.method == "POST":
        form = AdminBookingForm(request.POST)
        if form.is_valid():
            room = form.cleaned_data.get("room")
            checkin = form.cleaned_data.get("check_in")
            checkout = form.cleaned_data.get("check_out")
            form.save()
            messages.success(
                request, f"{room} has been booked from {checkin} to {checkout}"
            )
            return redirect("hotel:guest-list")
    else:
        form = AdminBookingForm()
    return render(request, "dashboard/create-booking.html", {"form": form})


def admin_payment(request):
    form = AdminPaymentForm()
    if request.method == "POST":
        form = AdminPaymentForm(request.POST)
        if form.is_valid():
            room = form.cleaned_data.get("booking")
            form.save()
            messages.success(request, f"{room} has been paid for successfully")
            return redirect("hotel:admin-payment-records")
    form = AdminPaymentForm()
    context = {"form": form}
    return render(request, "dashboard/create-payment.html", context)


def guest_detail(request, ref):
    guest = Booking.objects.get(reference_id=ref)
    room = guest.room
    user = guest.customer
    records = Booking.objects.filter(room=room, customer=user)
    context = {
        "guest": guest,
        "records": records,
    }
    return render(request, "dashboard/guest-detail.html", context)
