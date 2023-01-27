from django.contrib import admin

from .models import Room, Booking, RoomType

# Register your models here.


# class RoomImageInline(admin.TabularInline):
#     model = RoomImage
#     extra = 2


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    # inlines = [RoomImageInline]
    pass


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass
