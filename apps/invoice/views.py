from decimal import Decimal
from django.conf import settings

from django.http import HttpResponse

from django.shortcuts import render

from apps.invoice.forms import PaymentForm

from pypaystack import Transaction, Customer, Plan

from apps.invoice.models import Payment


# Create your views here.
def initiate_payment(request: HttpResponse) -> HttpResponse:
    amount = Decimal(request.session["amount"])
    email = request.user.email
    Payment.objects.create(amount=amount, email=email)
    context = {"amount": amount}
    return render(request, "hotel/initiate_payment.html", context)


def payment_records(request):
    payments = Payment.objects.all()
    context = {
        "payments": payments,
    }
    return render(request, "dashboard/payment-history.html", context)
