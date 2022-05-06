from django.shortcuts import render
from django.contrib.auth.models import User
import datetime
from RealEstateApp.models import Property
# Create your views here.


def AdminHome(request):
    count_users = User.objects.all().count()
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    month_from = datetime.datetime.now() - datetime.timedelta(days=30)
    count_property = Property.objects.all().count()
    last_day_count_users = User.objects.filter(
        date_joined__gte=date_from).count()
    last_month_count_users = User.objects.filter(
        date_joined__gte=month_from).count()
    last_day_count_property = Property.objects.filter(
        created__gte=date_from).count()
    last_month_count_property = Property.objects.filter(
        created__gte=month_from).count()

    print(last_day_count_property)
    print(last_month_count_property)
    context = {
        'count_users': count_users,
        'last_day_count_users': last_day_count_users,
        'last_month_count_users': last_month_count_users,
        'count_property': count_property,
        'last_day_count_property': last_day_count_property,
        'last_month_count_property': last_month_count_property,
    }
    return render(request, 'admin/adminDashboard.html', context)


def AdminManageUsers(request):
    admin_users = User.objects.filter(is_staff=True)
    print(admin_users[0].email)
    context = {
        'admin_users': admin_users
    }
    return render(request, 'admin/adminManageUser.html', context)
