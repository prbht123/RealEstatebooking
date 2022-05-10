from django.forms import ModelForm
from .models import Booking


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['gender', 'firstname', 'lastname', 'nationality', 'address', 'email', 'mobile_Number',
                  'property', 'date_from', 'date_until', 'creation_date', 'booking_status', 'cost', 'notes']


# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = Contact
#         fields = ['name','email','mobile_number','messages']