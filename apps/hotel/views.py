from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db import transaction
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
from apps.user.forms import StaffForm

from .availability import availability_checker, check_availability
from .decorators import active_staff_required, superuser_required
from .mixins import AdminRequiredMixin
from .models import Contact, Event, Room, Booking, RoomType

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
    RoomTypeForm,
)
from apps.hotel.utils import notification_email, send_contact_email

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


@superuser_required
def staff_list(request):
    staffs = User.objects.filter(staff=True)
    context = {"staffs": staffs}
    return render(request, "dashboard/staff-list.html", context)


@active_staff_required
def contact_list(request):
    contacts = Contact.objects.all()
    context = {"contacts": contacts}
    return render(request, "dashboard/contact-list.html", context)


# def update_staff_detail(request, pk):
#     profile = Profile.objects.get(slug=pk)
#     staff = User.objects.filter(profile=profile).first()
#     form = UpdateStaffDetailForm()
#     if request.method == 'POST':
#         form = UpdateStaffDetailForm(request.POST, request.FILES, instance=staff)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'{staff} Information updated successfully')
#             return redirect('hotel:dashboard')
#     context = {
#         'form': form
#     }
#     return render(request, 'dashboard/staff-update.html', context)


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


def admin_all_rooms(request):
    rooms = Room.objects.all()
    paginator = Paginator(rooms, 6)
    page_number = request.GET.get("page")
    page_number = page_number if page_number else 1
    try:
        current_page = paginator.page(page_number)
    except page_number.DoesNotExist:
        current_page = paginator.page(1)
    context = {"rooms": rooms, "page_obj": current_page}
    return render(request, "dashboard/rooms.html", context)


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


@superuser_required
def create_new_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "New Room Created Successfully.")
            return redirect("hotel:dashboard")
    context = {
        "form": form,
    }
    return render(request, "dashboard/create-room.html", context)


@superuser_required
def add_new_roomtype(request):
    form = RoomTypeForm()
    if request.method == "POST":
        form = RoomTypeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "New Room Type Added Successfully.")
            return redirect("hotel:dashboard")
    context = {
        "form": form,
    }
    return render(request, "dashboard/add-room-type.html", context)


@login_required
def check_bookings(request):
    user = request.user
    bookings = Booking.objects.filter(customer=user)
    context = {
        "bookings": bookings,
    }
    return render(request, "dashboard/booking-list.html", context)


@login_required
def payment_records(request):
    user = request.user
    payments = Payment.objects.filter(booking__customer=user)
    context = {
        "payments": payments,
    }
    return render(request, "hotel/payments-record.html", context)


@active_staff_required
def update_room(request, slug):
    room = get_object_or_404(Room, slug=slug)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "Room Updated Successfully")
            return redirect("hotel:dashboard")
    else:
        form = RoomForm(instance=room)
    return render(request, "dashboard/create-room.html", {"form": form})


@active_staff_required
def update_payment(request, ref):
    payment = get_object_or_404(Payment, ref=ref)
    if request.method == "POST":
        form = AdminPaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect("hotel:admin-payment-records")
    else:
        form = AdminPaymentForm(instance=payment)
    return render(request, "dashboard/update_payment.html", {"form": form})


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


@superuser_required
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "New Room Created Successfully.")
            return redirect("hotel:dashboard")
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
        return reverse("dashboard:room-records")


@login_required
def book_room(request, slug):
    room = Room.objects.get(slug=slug)
    form = BookingForm()
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            checkin = form.cleaned_data["check_in"]
            checkout = form.cleaned_data["check_out"]
            # if room.is_available
            if availability_checker(room, checkin, checkout):
                booking = form.save(commit=False)
                booking.room = room
                booking.customer = request.user
                booking.save()
                room.is_available = False
                room.save()
                subject = "Confirmation of Your Reservation at FreshKom4tHotel"
                user = request.user
                notification_email(
                    user, subject, booking, template="hotel/booking_notice_email.html"
                )
                messages.success(request, "Room has been Booked Successfully.")
                return redirect("hotel:booking-list")
            else:
                messages.error(
                    request, "Sorry! Room has already been booked for selected date."
                )
                return redirect("hotel:book-room", slug)
    return render(request, "hotel/book_room.html", {"room": room, "form": form})


@login_required
def book_and_pay_room(request, slug):
    room = Room.objects.get(slug=slug)
    form = BookingForm()
    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            checkin = form.cleaned_data["check_in"]
            checkout = form.cleaned_data["check_out"]

            if availability_checker(room, checkin, checkout):
                try:
                    # Use a try-except block to handle potential database errors
                    with transaction.atomic():
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
                    messages.success(request, "Room has been booked successfully.")
                    return render(request, "hotel/initiate_payment.html", context)
                except Exception as e:
                    messages.error(request, "An error occurred while booking the room. Please try again later.")
            else:
                extra = "Book another room or choose another date."
                messages.error(request, f"Sorry! Room has already been booked for the selected date. {extra}")
                return redirect("hotel:book-room", slug)
    
    return render(request, "hotel/book-pay-room.html", {"room": room, "form": form})


@active_staff_required
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

@active_staff_required
def guest_list(request):
    guests = Booking.objects.all()
    context = {
        "guests": guests,
    }
    return render(request, "dashboard/guest-list.html", context)


@active_staff_required
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


@active_staff_required
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


@active_staff_required
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


@active_staff_required
def admin_payment_records(request):
    payments = Payment.objects.all()

    context = {
        "payments": payments,
    }
    return render(request, "dashboard/admin-payment-records.html", context)


@active_staff_required
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


@superuser_required
def add_new_staff(request):
    form = StaffForm()
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            messages.success(request, "New Staff has been Added Successfully")
            form.save()
            return redirect("hotel:staff-list")
    context = {"form": form}
    return render(request, "dashboard/create-staff.html", context)


def room_type(request, slug):
    types = RoomType.objects.get(slug=slug)
    rooms = Room.objects.filter(room_type=types)

    context = {
        'rooms': rooms,
        'type': types
    }
    return render(request, 'dashboard/room-type.html', context)    