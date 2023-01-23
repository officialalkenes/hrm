from django import forms

from .models import Room, Booking


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
