from datetime import datetime, timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib import messages

from django.http import HttpResponse

from django.shortcuts import redirect, render

from apps.invoice.forms import AdminPaymentForm, PaymentForm

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
    return render(request, "dashboard/payment-records.html", context)


# # views
# def check_available_hours(request):
#     day_request = request.GET.get('day','') #day in format yyyy-MM-dd
#     date_of_reference = datetime.strptime(day_request, "%Y-%m-%d")
#     initial_date_time = date_of_reference
#     final_date_time = date_of_reference + timedelta(hours=23)
#     appointments_of_day = Appointment.objects.filter(
#         start_appointment__gte=initial_date_time,
#         start_appointment__lte=final_date_time
#     )
#     reserved_times = [
#     appointment.start_appointment + timedelta(minutes=10*i) for appointment in appointments_of_day for i in range((appointment.end_appointment - appointment.start_appointment).seconds//600)]
#     # same as above but more undestandeble
# # for appointment in appointments_of_day:
# #     for i in range((appointment.end_appointment - appointment.start_appointment)//600):
# #         reserved_times.append(appointment.start_appointment + timedelta(minutes=10*i))
#     hours_between = [initial_date_time + timedelta(minutes=10*i) for i in range(((final_date_time - initial_date_time).seconds // 600) + 1)]
#     avaliable_hours = [hour.time() for hour in hours_between if hour not in reserved_times]

#     return render(request, "name_template.html", {"hours": avaliable_hours})


def get_available_slots(event, date):
    # Get all appointments for the doctor on the given date
    appointments = Payment.objects.filter(event=event, start_time__date=date)

    # Create a list of unavailable time slots
    unavailable_slots = [
        (appointment.start_time, appointment.end_time) for appointment in appointments
    ]

    # Check if desired time slot overlaps with any of the unavailable slots
    def is_slot_available(desired_start, desired_end):
        for start, end in unavailable_slots:
            if desired_start >= start and desired_start < end:
                return False
            if desired_end > start and desired_end <= end:
                return False
        return True

    desired_start = datetime(2022, 1, 1, 9, 0)  # 9:00 AM
    desired_end = datetime(2022, 1, 1, 9, 30)  # 9:30 AM
    if is_slot_available(desired_start, desired_end):
        print("Time slot is available")
    else:
        print("Time slot is not available")


def create_payment(request):
    form = AdminPaymentForm()
    if request.method == "POST":
        form = AdminPaymentForm()
        if form.is_valid():
            form.save()
            messages.success(request, "New Payment Has been Added")
            return redirect("invoice:payment-records")
    context = {}
    return render(request, "", context)
