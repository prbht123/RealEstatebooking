from audioop import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import datetime
from BookingApp.models import Booking
from RealEstateApp.models import Property
from .forms import AdminUserRegistrationForm, AdminUserRolesForm
from .models import AdminUserRoles
from django.views.generic import UpdateView, CreateView, ListView, DeleteView
# Create your views here.


def adminHome(request):
    """
        Admin dashboard page.
    """
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


def adminManageUsers(request):
    """
        List out the all admin users.
    """
    admin_users = User.objects.filter(is_staff=True)
    print(admin_users[0].email)
    context = {
        'admin_users': admin_users
    }
    return render(request, 'admin/adminManageUser.html', context)


def adminRegisterUser(request):
    """
        Admin user can register new admin users.
    """
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


def deleteAdminUser(request, pk):
    """
        Admin user can remove admin users and add as a normal user.
    """
    try:
        user = User.objects.get(id=pk)
        user.is_staff = False
        user.save()
        return redirect('admin_user:manage_users')
    except Exception as e:
        raise e


class createRoleAdmin(CreateView):
    """
        Admin user can add the roles to particular admin users.
    """
    form_class = AdminUserRolesForm
    template_name = 'admin/roles/create_role_admin_user.html'

    def form_valid(self, form):
        data = form.save(commit=False)
        user = User.objects.get(id=self.kwargs['pk'])
        data.user = user
        data.save()
        return redirect('/')


class roleUpdateView(UpdateView):
    """
        Admin users can update the roles of admin users.
    """
    model = AdminUserRoles
    form_class = AdminUserRolesForm
    template_name = 'admin/roles/create_role_admin_user.html'
    success_url = '/adminuser/manageuser'

    def get_form_kwargs(self):
        kwargs = super(roleUpdateView, self).get_form_kwargs()
        kwargs.update()
        return kwargs


class adminManageUsersRoles(ListView):
    """
        Admin users can see the all roles with admin users.
    """
    template_name = 'admin/roles/manage_admin_user_roles.html'
    model = AdminUserRoles
    context_object_name = 'adminuserroles'


class deleteAdminUserRoles(DeleteView):
    """
        Admin users can delete the roles of admin users.
    """
    model = AdminUserRoles
    template_name = 'admin/roles/delete_admin_user_roles.html'
    success_url = '/adminuser/manageuser'
