from django import forms

from apps.profiles.models import StaffProfile


class CreateStaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = "__all__"
