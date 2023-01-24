from django import forms

from django.forms import inlineformset_factory

from .models import Room, Booking, RoomImage


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
            "room_name",
            "room_number",
            "room_type",
            "price",
            "capacity",
            "beds",
            "image",
            "description",
            "is_available",
        )


class EventForm(forms.ModelForm):
    pass
