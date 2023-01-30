from django.http import HttpResponse

from django.shortcuts import render


# Create your views here.
def initiate_payment(request: HttpResponse) -> HttpResponse:
    if request.method == "POST":
        ...
