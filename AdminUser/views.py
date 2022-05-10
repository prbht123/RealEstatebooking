from audioop import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import datetime
from BookingApp.models import Booking
from RealEstateApp.models import Property
from .forms import AdminUserRegistrationForm
from django.views.generic import UpdateView
# Create your views here.


def AdminHome(request):
    count_users = User.objects.all().count()
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    month_from = datetime.datetime.now() - datetime.timedelta(days=30)
    count_property = Property.objects.all().count()
    count_booking = Booking.objects.all().count()
    last_day_count_users = User.objects.filter(
        date_joined__gte=date_from).count()
    last_month_count_users = User.objects.filter(
        date_joined__gte=month_from).count()
    last_day_count_property = Property.objects.filter(
        created_date__gte=date_from).count()
    last_month_count_property = Property.objects.filter(
        created_date__gte=month_from).count()
    last_day_count_booking = Booking.objects.filter(
        creation_date__gte=date_from).count()
    last_month_count_booking = Booking.objects.filter(
        creation_date__gte=month_from).count()

    context = {
        'count_users': count_users,
        'last_day_count_users': last_day_count_users,
        'last_month_count_users': last_month_count_users,
        'count_property': count_property,
        'last_day_count_property': last_day_count_property,
        'last_month_count_property': last_month_count_property,
        'count_booking': count_booking,
        'last_day_count_booking': last_day_count_booking,
        'last_month_count_booking': last_month_count_booking
    }
    return render(request, 'admin/adminDashboard.html', context)


def AdminManageUsers(request):
    admin_users = User.objects.filter(is_staff=True)
    print(admin_users[0].email)
    context = {
        'admin_users': admin_users
    }
    return render(request, 'admin/adminManageUser.html', context)


def AdminRegisterUser(request):
    if request.method == 'POST':
        user_form = AdminUserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_staff = True
            # Save the User object
            new_user.save()
        else:
            error = "This user is already exist"
            return render(request, 'registration/create_admin_register_user.html', {'user_form': user_form, 'error': error})

        return render(request, 'registration/admin_register_user_done.html', {'new_user': new_user})
    else:
        user_form = AdminUserRegistrationForm()
        return render(request, 'registration/create_admin_register_user.html', {'user_form': user_form})


def DeleteAdminUser(request, pk):
    try:
        user = User.objects.get(id=pk)
        user.is_staff = False
        user.save()
        return redirect('admin_user:manage_users')
    except Exception as e:
        raise e
