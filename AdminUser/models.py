from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django_countries.fields import CountryField
# Create your models here.


class AdminUserRoles(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=500)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="admin_user_role")
    roles = models.ForeignKey(
        Permission, on_delete=models.CASCADE, null=True, related_name='roles')

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(AdminUserRoles, self).save(*args, **kwargs)


class PopularLocations(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=250, null=True)
    state = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    country = CountryField(null=True)
    popular_rank = models.IntegerField(null=True)

    def __str__(self):
        return self.city

    def save(self, *args, **kwargs):
        self.slug = slugify(self.city)
        super(PopularLocations, self).save(*args, **kwargs)
