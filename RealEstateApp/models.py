from django.db import models
import uuid
from taggit.managers import TaggableManager
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    room_type_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250)

    def __str__(self):
        return self.room_type_name


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    street = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=250, null=True)
    state = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    country = CountryField(null=True)
    zip_code = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.city

    def save(self, *args, **kwargs):
        self.slug = slugify(self.street)
        super(Address, self).save(*args, **kwargs)


class Property(models.Model):
    STATUS_BED_TYPE = (
        ('adult', 'Adult'),
        ('child', 'Child'),
        ('both', 'Both')
    )
    STATUS_PROPERTY = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    STATUS_CANCELLATION = (
        ('free', 'Free'),
        ('paid', 'Paid')
    )
    id = models.AutoField(primary_key=True)
    property_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='property_posts')
    image = models.ImageField(
        upload_to='property/images/', blank=True, null=True)
    room_type = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='room_type')
    bed_room = models.IntegerField()
    beds = models.IntegerField()
    bed_type = models.CharField(
        max_length=10, choices=STATUS_BED_TYPE, default='adult')
    guest = models.IntegerField()
    Address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name='address')
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    property_status = models.CharField(
        max_length=10, choices=STATUS_PROPERTY, default='draft')
    contact_number = models.BigIntegerField()
    cancellation = models.CharField(
        max_length=10, choices=STATUS_CANCELLATION, default='free')
    Description = models.TextField()
    # features=TaggableManager()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.property_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.property_name)
        super(Property, self).save(*args, **kwargs)


class MostViewed(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='view_property')
    viewed = models.BigIntegerField()

    def __str__(self):
        return self.property.property_name


class FeedBackProperty(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=250)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='feedback')
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE)
    feedback = models.TextField()

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.property.property_name)
        super(FeedBackProperty, self).save(*args, **kwargs)


class RankingProperty(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=250)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ranking')
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE)
    rank = models.IntegerField(default=1, blank=True, null=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.property.property_name)
        super(RankingProperty, self).save(*args, **kwargs)


class ImagesProperty(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=250)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='property/item/images/', blank=True, null=True)

    def __str__(self):
        return self.property.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.property.property_name)
        super(ImagesProperty, self).save(*args, **kwargs)
