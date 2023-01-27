from django import forms

from django.forms import inlineformset_factory

from .models import Contact, Room, Booking, RoomImage


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


RoomImageFormset = inlineformset_factory(
    Room,
    RoomImage,
    fields=[
        "image",
    ],
    extra=2,
)


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = (
            "room_number",
            "room_type",
            "price",
            "capacity",
            "beds",
            "image",
            "description",
            "is_available",
        )


class RoomImageForm(forms.ModelForm):
    class Meta:
        model = RoomImage
        fields = ("image",)


class RoomAvailabilityForm(forms.ModelForm):
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
    room_number = forms.ChoiceField(choices=ROOM_NUMBER, required=True)
    people = forms.ChoiceField(choices=PEOPLE, required=True)
    check_in = forms.DateField()
    check_out = forms.DateField()


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("name", "email", "subject", "message")


class EventForm(forms.ModelForm):
    pass
