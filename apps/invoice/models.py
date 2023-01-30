import secrets
from django.db import models

# Create your models here.


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return f"Payment Ref: {self.ref}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_same_ref = self.objects.filter(ref=ref)
            if not object_with_same_ref:
                self.ref = ref
        return super().save(*args, **kwargs)


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
