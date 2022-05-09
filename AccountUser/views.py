from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserProfileForm
from .models import UserProfile
from RealEstateApp.models import Address
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView
# Create your views here.


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()

        return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'user_form': user_form})


def UserProfileView(request):
    return render(request, 'home.html')


class CreateUserProfileView(CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'user/create_user_profile.html'

    def form_valid(self, form):
        first_name = self.request.POST['first_name']
        last_name = self.request.POST['last_name']
        street = self.request.POST['street']
        city = self.request.POST['city']
        state = self.request.POST['state']
        country = self.request.POST['country']
        zip_code = self.request.POST['zip_code']
        address = Address.objects.create(
            street=street, city=city, state=state, country=country, zip_code=zip_code)
        address.save()
        print(first_name)
        user = User.objects.get(id=self.request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        data = form.save(commit=False)
        data.user = user
        data.address = address
        data.image = self.request.FILES['myFile']
        data.save()
        return redirect('/')
