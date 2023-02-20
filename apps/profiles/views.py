from django.shortcuts import render


def create_staff_profile(request):
    context = {}
    return render(request, "dashboard/create_staff_profile.html", context)
