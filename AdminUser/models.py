from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
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
