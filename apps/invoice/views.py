from django.conf import settings

from django.http import HttpResponse

from django.shortcuts import render

from apps.invoice.forms import PaymentForm

from pypaystack import Transaction, Customer, Plan


# Create your views here.
def initiate_payment(request: HttpResponse) -> HttpResponse:
    if request.method == "POST":
        payment = PaymentForm(request.POST)
        if payment.is_valid():
            payment = payment.save()
    payment = PaymentForm()
    context = {"payment": payment}
    return render(request, "hotel/initiate_payment.html", context)
