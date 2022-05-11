from django.contrib import admin
from .models import Address, Property, Room, MostViewed, FeedBackProperty, RankingProperty
# Register your models here.


admin.site.register(Property)
admin.site.register(Room)
admin.site.register(Address)
admin.site.register(MostViewed)
admin.site.register(FeedBackProperty)
admin.site.register(RankingProperty)
