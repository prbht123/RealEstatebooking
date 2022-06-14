from multiprocessing import get_context
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserProfileForm
from .models import UserProfile
from RealEstateApp.models import Address, Property, RankingProperty, MostViewed, FeedBackProperty
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.db.models import Avg, Count
from django.urls import reverse

# Create your views here.


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        print("99999999999999999999999999999999999")
        print(request.POST.get('option1'))
        print("pppppppppppppppppppppppppppppppppp")
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            if request.POST.get('option1'):
                new_user.save()
            else:
                msg = "please click agrred"
                print(msg)
                return render(request, 'registration/signup.html', {'user_form': user_form, 'msg': msg})

        return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'registration/signup.html', {'user_form': user_form})


def homeView(request):
    user = UserProfile.objects.filter(user__id=request.user.id)
    print(request.user)
    return redirect('/')
    # return render(request, 'user/user_profile.html', {'user': user})


class UserProfileDetailView(ListView):
    model = UserProfile
    template_name = 'user/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userprofile'] = UserProfile.objects.get(
            user__id=self.request.user.id)
        return context


def UserProfileView(request, pk):
    userprofile = UserProfile.objects.filter(user=request.user)
    property = Property.objects.filter(author=request.user)
    property_count = property.count()
    print(property_count)
    approved_property = Property.objects.filter(
        author=request.user, property_status='published').count()
    draft_property = Property.objects.filter(
        author=request.user, property_status='draft').count()
    most_ranking_property = RankingProperty.objects.filter(
        property__author=request.user, property__property_status='published')
    if most_ranking_property:
        ranking_property_list = most_ranking_property.values(
            'property__property_name').annotate(avg=Avg('rank')).order_by('-avg')
        most_ranking_property = ranking_property_list[0]
    property_list = []
    if property:
        for item in property:
            data = {}
            if most_ranking_property:
                if ranking_property_list:
                    property_list_rating = ranking_property_list.filter(
                        property__property_name=item.property_name)
                    print(property_list_rating)
                    if property_list_rating:
                        data = {
                            'property': item,
                            'rating': "{:.1f}".format(property_list_rating[0]['avg'])
                        }
            if not data:

                data = {
                    'property': item,
                    'rating': 0
                }
            property_list.append(data)

    most_viewed_property = MostViewed.objects.filter(
        property__property_status='published', property__author=request.user).order_by('-viewed')
    if most_viewed_property:
        most_viewed_property = most_viewed_property[0]

    if userprofile:
        return render(request, 'user/owner_profile.html', {'userprofile': userprofile[0], 'property': property_list, 'approved_property': approved_property, 'draft_property': draft_property, 'most_ranking_property': most_ranking_property, 'most_viewed_property': most_viewed_property, 'property_count': property_count, })
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
        # return redirect('/')
        return redirect(reverse('account:user_profile', kwargs={'pk': user.id}))


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
    return redirect('/home/')
