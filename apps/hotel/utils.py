import random
import string
import secrets

from smtplib import SMTPException
from socket import gaierror

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

import apps.hotel.models as models


def generate_unique_pass():
    return secrets.token_hex(4)


def generate_unique_reference():
    reference_number = generate_unique_pass()
    while True:
        try:
            models.Booking.objects.get(reference=reference_number)
            reference_number = generate_unique_pass()
        except models.Booking.DoesNotExist:
            break
    return reference_number


def send_contact_email(name, email, subject, content, template):
    message = render_to_string(
        template,
        {"email": email, "name": name, "content": content},
    )
    try:
        send_mail(subject, message, email, [settings.DEFAULT_FROM_EMAIL])
        return "success"
    except (ConnectionAbortedError, SMTPException, gaierror):
        return "error"


def notification_email(user, subject, booking, template):
    message = render_to_string(
        template,
        {"email": user.email, "user": user, "booking": booking},
    )
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [
                user.email,
            ],
        )
        return "success"
    except (ConnectionAbortedError, SMTPException, gaierror):
        return "error"
