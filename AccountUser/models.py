import imp
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from RealEstateApp.models import Address
# Create your models here.


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_profile')
    slug = models.SlugField(max_length=250)
    contact_number = models.BigIntegerField()
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='user/images/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)
