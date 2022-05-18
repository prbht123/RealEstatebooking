from multiprocessing import get_context
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserProfileForm
from .models import UserProfile
from RealEstateApp.models import Address
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, DetailView, UpdateView
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


def homeView(request):
    user = UserProfile.objects.filter(user=request.user)
    print(request.user)
    return redirect('/')
    # return render(request, 'user/user_profile.html', {'user': user})


def UserProfileView(request, pk):
    userprofile = UserProfile.objects.filter(user=request.user)
    if userprofile:
        return render(request, 'user/userprofile_list.html', {'userprofile': userprofile[0]})
    else:
        return redirect('account:create_user_profile')


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


class UpdateProfileView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'user/update_user_profile.html'
    success_url = '/'

    def get_form_kwargs(self, **kwargs):
        print(self.request.POST.get('first_name'))
        kwargs = super(UpdateProfileView, self).get_form_kwargs()
        address = Address.objects.get(id=kwargs['instance'].address.id)
        address.city = self.request.POST.get('city')
        address.street = self.request.POST.get('street')
        address.state = self.request.POST.get('state')
        address.country = self.request.POST.get('country')
        address.zip_code = self.request.POST.get('zip_code')
        address.save()
        user = User.objects.get(id=kwargs['instance'].user.id)
        # user.first_name = self.request.POST.get('first_name')
        # user.last_name = self.request.POST.get('last_name')
        # user.save()
        kwargs['instance'].user = user
        kwargs['instance'].address = address
        if self.request.FILES:
            kwargs['instance'].image = self.request.FILES['myFile']
        # kwargs['instance'].address.save()
        kwargs.update()
        return kwargs


def UserDeleteView(request, slug):
    userprofile = UserProfile.objects.get(slug=slug)
    user = User.objects.get(id=userprofile.user.id)
    user.delete()
    return redirect('/')
