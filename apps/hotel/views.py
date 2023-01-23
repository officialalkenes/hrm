from django.shortcuts import render

from .models import Room, Booking


def homepage(request):
    context = {}
    return render(request, "", context)
