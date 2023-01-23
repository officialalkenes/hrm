from django.db import models

from django.utils.translation import gettext_lazy as _


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=100, verbose_name=_("Hotel Name"))


class Rooms(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name=_("hotel"))
