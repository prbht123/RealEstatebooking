from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models import DateTimeField
from django.utils import timezone
import uuid
from RealEstateApp.models import Address, Property
from django.utils.text import slugify
#from RealEstate_App.models import Address, Property


# Create your models here.

# class Address(models.Model):
#     uuid = models.UUIDField(
#         primary_key=True, default=uuid.uuid4, unique=True, editable=False)
#     street = models.TextField()
#     city = models.TextField()
#     province = models.TextField()
#     zip_code = models.TextField()

#     def __str__(self):
#         return self.street


STATUS_BOOKING = (
    ('initiated', 'Initiated'),
    ('pending', 'Pending'),
    ('confirm', 'Confirm'),
    ('cancel', 'Cancel'),
    ('completed', 'Completed')
)


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)


class Booking(models.Model):

    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=250)
    gender = models.CharField(
        max_length=100, choices=GENDER_CHOICES, default='M')
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=30)
    nationality = CountryField(blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50)
    mobile_Number = models.BigIntegerField()
    date_from = models.DateTimeField()
    date_until = models.DateTimeField()
    creation_date = models.DateTimeField(default=timezone.now, null=True)
    updated_date = models.DateTimeField(auto_now=True)
    #created_date = models.DateTimeField(auto_now_add=True)
    booking_status = models.CharField(
        max_length=100, choices=STATUS_BOOKING, default='initiated')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    paid = models.BooleanField(default=False)
    notes = models.TextField()



class Contact(models.Model):
    def save(self, *args, **kwargs):
        self.slug = slugify(self.property.property_name)
        super(Booking, self).save(*args, **kwargs)


class ContactDetails(models.Model):
    name = models.CharField(max_length=100, null=True, verbose_name='Name')
    email = models.EmailField(null=True)
    mobile_number = models.BigIntegerField(null=True)
    messages = models.TextField(null=True)
    def __str__(self):
        return f"{ self.email }" 

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.property.property_name)
    #     super(Booking, self).save(*args, **kwargs)

    def __str__(self):
        return f"{ self.email }"

