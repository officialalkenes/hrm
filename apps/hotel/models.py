from django.contrib.auth import get_user_model

from django.db import models

from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    room_number = models.CharField(max_length=255, unique=True)
    room_type = models.CharField(max_length=255)
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
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=255)
