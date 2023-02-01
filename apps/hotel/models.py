import random
import string


from django.contrib.auth import get_user_model

from django.db import models

from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .utils import generate_unique_pass, generate_unique_reference

User = get_user_model()


def room_type_image_path(instance, filename):
    return f"rooms/{instance.types}/{filename}"


def room_image_path(instance, filename):
    return f"rooms/{instance.room_number}/{instance.room_type.types}/{filename}"


class RoomType(models.Model):
    types = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    image_repr = models.ImageField(upload_to=room_type_image_path)

    def __str__(self):
        return f"{self.types}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.types)
        return super().save(self, *args, **kwargs)


class Room(models.Model):
    room_number = models.CharField(max_length=255, unique=True)
    room_type = models.ForeignKey(
        RoomType, on_delete=models.CASCADE, related_name=_("+")
    )
    slug = models.SlugField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField(verbose_name=_("Maximum People per room"))
    beds = models.PositiveIntegerField(verbose_name=_("Number of Beds"))
    image = models.ImageField(upload_to=room_image_path)
    description = models.TextField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_number} - {self.room_type}"

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.room_type.types}-{self.room_number}")
        return super().save(self, *args, **kwargs)


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name=_("+"))
    reference_id = models.CharField(max_length=100, unique=True, blank=True)
    check_in = models.DateField()
    check_out = models.DateField()
    preferred_entry_time = models.TimeField(null=True)
    has_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=255)
    has_checked_out = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.room} - {self.check_in} to {self.check_out}"

    @property
    def days_difference(self):
        return (self.check_out - self.check_in).days + 1

    @property
    def get_total_amount(self):
        total = self.days_difference * self.room.price
        return total

    def save(self, *args, **kwargs):
        if self.reference_id == "":
            self.reference_id = generate_unique_pass()
        return super().save(*args, **kwargs)


class Event(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name=_("+"))
    name = models.CharField(
        max_length=100, verbose_name=_("Event"), help_text=_("event: bridal shower")
    )
    slug = models.SlugField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField(verbose_name=_("Maximum People per room"))


class EventBooking(models.Model):
    hall = models.ForeignKey(Event, on_delete=models.CASCADE, related_name=_("+"))
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name=_("+"))
    check_in = models.DateField()
    check_out = models.DateField()
    preferred_entry_time = models.TimeField()
    default_exit_time = models.TimeField()
    status = models.CharField(max_length=255)
    has_checked_out = models.BooleanField(default=False)

    @property
    def get_days(self):
        if (self.check_out - self.check_in).days() == 0:
            return 1
        return (self.check_out - self.check_in).days()


class BookingRefund(models.Model):
    guest = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Booking, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return str(self.guest)


class RoomServices(models.Model):
    # service = models.()
    current_booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name=_("+")
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name=_("+"))

    def __str__(self) -> str:
        return f"{self.room}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.subject}"
