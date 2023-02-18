import secrets
from django.db import models

from django.contrib.auth import get_user_model


User = get_user_model()


class Payment(models.Model):
    PAYMENT_TYPE = (
        ("CASH", "Cash"),
        ("CARD", "Credit/Debit Card"),
        ("ONLINE", "Online Payment"),
        ("BANK", "Bank Transfer"),
        ("INVOICE", "Invoice"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=100, choices=PAYMENT_TYPE)
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return f"Payment Ref: {self.ref} - {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_same_ref = Payment.objects.filter(ref=ref)
            if not object_with_same_ref:
                self.ref = ref
        return super().save(*args, **kwargs)

    @property
    def amount_value(self) -> float:
        return self.amount * 100


# class HallType(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.CharField(max_length=1024, null=True, blank=True)

#     def __str__(self):
#         return self.name


# class Hall(models.Model):
#     number = models.CharField(max_length=6)
#     name = models.CharField(max_length=100)
#     hall_type = models.ForeignKey(HallType, on_delete=models.CASCADE)
#     price_per_night = models.DecimalField(max_digits=20, decimal_places=2)
#     max_capacity = models.PositiveIntegerField()
#     marked_for_housekeep = models.BooleanField(default=False)

#     def __str__(self):
#         return self.name


class Event(models.Model):
    ...


class Schedule(models.Model):
    # event=models.ForeignKey(Event)
    open = models.TimeField()
    close = models.TimeField()
