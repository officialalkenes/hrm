from django import forms

from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ("amount", "email")


class AdminPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"
