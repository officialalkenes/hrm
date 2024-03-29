from django import forms

from django.forms import inlineformset_factory

from apps.invoice.models import Payment

from .models import Contact, Room, Booking, RoomType


class AvailabilityForm(forms.Form):
    ...
    ROOM_CATEGORY = ()
    room_category = forms.ChoiceField(choices=ROOM_CATEGORY, required=True)
    check_in = forms.DateField()
    check_out = forms.DateField()

    class Meta:
        widgets = {
            "check_in": forms.TextInput(attrs={"type": "date"}),
            "check_out": forms.TextInput(attrs={"type": "date"}),
        }


class RoomDetailAvailabilityForm(forms.Form):
    room = forms.CharField(max_length=100)
    check_in = forms.DateField()
    check_out = forms.DateField()

    class Meta:
        widgets = {
            "check_in": forms.TextInput(attrs={"type": "date"}),
            "check_out": forms.TextInput(attrs={"type": "date"}),
        }


# RoomImageFormset = inlineformset_factory(
#     Room,
#     RoomImage,
#     fields=[
#         "image",
#     ],
#     extra=2,
# )


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ("slug",)


class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        exclude = ("slug",)


# class RoomImageForm(forms.ModelForm):
#     class Meta:
#         model = RoomImage
#         fields = ("image",)


class RoomAvailabilityForm(forms.Form):
    ROOM_NUMBER = (
        (1, 1),
        (2, 2),
        (3, 3),
    )
    PEOPLE = (
        (1, 1),
        (2, 2),
    )
    # room = forms.InlineForeignKeyField(RoomForm)
    beds = forms.ChoiceField(choices=ROOM_NUMBER, required=True)
    people = forms.ChoiceField(choices=PEOPLE, required=True)
    check_in = forms.DateField(
        widget=forms.DateInput(attrs={"class": "date-input", "id": "date-in"})
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={"class": "date-input", "id": "date-out"})
    )


class BookingForm(forms.ModelForm):
    check_in = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "date-input input--style-1", "id": "date-in"}
        )
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={"class": "date-input", "id": "date-out"})
    )

    class Meta:
        model = Booking
        fields = ("check_in", "check_out")


class AdminBookingForm(forms.ModelForm):
    check_in = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "date-input input--style-1", "id": "date-in"}
        )
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={"class": "date-input", "id": "date-out"})
    )

    class Meta:
        model = Booking
        fields = "__all__"


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("name", "email", "subject", "message")


class EventForm(forms.ModelForm):
    pass


class AdminPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"
