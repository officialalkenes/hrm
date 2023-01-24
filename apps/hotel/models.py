from django.contrib.auth import get_user_model

from django.db import models

from django.utils.translation import gettext_lazy as _

User = get_user_model()


class RoomType(models.Model):
    types = models.CharField(max_length=100)


class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    room_number = models.CharField(max_length=255, unique=True)
    room_type = models.ForeignKey(
        RoomType, on_delete=models.CASCADE, related_name=_("+")
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField(verbose_name=_("Maximum People per room"))
    beds = models.PositiveIntegerField(verbose_name=_("Number of Beds"))
    image = models.ImageField(upload_to="rooms/")
    description = models.TextField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.room_name


class RoomImage(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name=_("room_image")
    )
    image = models.ImageField(blank=True)

    def __str__(self) -> str:
        return f"{self.room.room_name}"


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name=_("client")
    )
    check_in = models.DateField()
    check_out = models.DateField()
    preferred_entry_time = models.TimeField()
    default_exit_time = models.TimeField()
    status = models.CharField(max_length=255)
    has_checked_out = models.BooleanField(default=False)

    @property
    def days_difference(self):
        return (self.checked_out - self.check_in).days

    @property
    def get_price_per_difference(self):
        total = self.days_difference * self.room.price
        return total


class HallBooking(models.Model):
    hall = ""
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name=_("client")
    )
    check_in = models.DateField()
    check_out = models.DateField()
    preferred_entry_time = models.TimeField()
    default_exit_time = models.TimeField()
    status = models.CharField(max_length=255)
    has_checked_out = models.BooleanField(default=False)
