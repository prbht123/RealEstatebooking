from django.contrib import admin
from .models import Address, Property, Room
# Register your models here.


admin.site.register(Property)
admin.site.register(Room)
admin.site.register(Address)
