from django.db import models

# Create your models here.


class HallType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.name


class Hall(models.Model):
    number = models.CharField(max_length=6)
    name = models.CharField(max_length=100)
    hall_type = models.ForeignKey(HallType, on_delete=models.CASCADE)
    price_per_night = models.DecimalField(max_digits=20, decimal_places=2)
    max_capacity = models.PositiveIntegerField()
    marked_for_housekeep = models.BooleanField(default=False)

    def __str__(self):
        return self.name
