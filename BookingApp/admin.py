from django.contrib import admin
from .models import Booking,Contact,ContactDetails

# Register your models here.
admin.site.register(Booking)
admin.site.register(Contact)

admin.site.register(ContactDetails)
