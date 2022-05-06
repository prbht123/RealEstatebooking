from django.shortcuts import render
from django.contrib.auth.models import User
import datetime
# Create your views here.


def AdminHome(request):
    count_users = User.objects.all().count()
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    month_from = datetime.datetime.now() - datetime.timedelta(days=30)
    last_day_count_users = User.objects.filter(
        date_joined__gte=date_from).count()
    last_month_count_users = User.objects.filter(
        date_joined__gte=month_from).count()
    context = {
        'count_users': count_users,
        'last_day_count_users': last_day_count_users,
        'last_month_count_users': last_month_count_users,
    }
    return render(request, 'admin/adminDashboard.html', context)


def AdminManageUsers(request):
    admin_users = User.objects.filter(is_staff=True)
    print(admin_users[0].email)
    context = {
        'admin_users': admin_users
    }
    return render(request, 'admin/adminManageUser.html', context)
