from django.contrib import admin

from .models import User, Room, RoomType, Facility, Reservation, Customer, CheckOut, CheckIn

# Register your models here.
admin.site.register(User)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(Facility)
admin.site.register(Reservation)
admin.site.register(Customer)
admin.site.register(CheckOut)
admin.site.register(CheckIn)