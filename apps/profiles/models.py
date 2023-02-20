from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class StaffProfile(models.Model):
    POSITION = (
        ("admin", "Administrator"),
        ("staff", "Staff"),
        ("guest", "Guest"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # salary = models.DecimalField(null=True, blank=True)
    position = models.CharField(max_length=100, choices=POSITION)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateField()

    def __str__(self) -> str:
        return f"{self.user.email}"
