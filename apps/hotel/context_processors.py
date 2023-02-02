from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from django.db.models import Sum

from .models import Room

User = get_user_model()


def dashboard_context(request):
    current_site = get_current_site(request)

    if request.user.is_authenticated:
        user = User.objects.all()
        all_rooms = Room.objects.all()
        return {
            "current_site": current_site,
            "all_rooms": len(all_rooms),
            "total_guests": len(user),
            "available_rooms_count": len(all_rooms.filter(is_available=True)),
            "booked_rooms_count": len(all_rooms.filter(is_available=False)),
        }
    else:
        return {"": ""}
