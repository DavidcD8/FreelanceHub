from django.shortcuts import render, get_object_or_404, redirect

from create_superuser import User
from .models import Service, Profile, UserRating
from .forms import ServiceForm, UserRatingForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from .forms import ProfileForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log the user in after registration
            return redirect('home')  # or any other page
        return render(request, 'registration/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})



def home(request):
    services = Service.objects.all().order_by('-created')[:6]
    categories = Service.CATEGORY_CHOICES
    for service in services:
        avg = getattr(service.owner.profile, 'average_rating', None)
        if avg:
            filled = int(round(avg))
            empty = 5 - filled
        else:
            filled = 0
            empty = 5
        service.filled_stars = range(filled)
        service.empty_stars = range(empty)
    return render(request, 'home.html', {'services': services, 'categories': categories})



def profile_view(request):
    # Show logged-in user's profile
    user = request.user
    profile = user.profile
    services = user.service_set.all()
    context = {
        'user_profile': profile,
        'services': services,
    }
    return render(request, 'profile.html', context)



def view_other_profile(request, username):
    user_profile = get_object_or_404(Profile, user__username=username)
    user_services = Service.objects.filter(owner=user_profile.user)
    average_rating = user_profile.average_rating
  

    context = {
        "recipient": user_profile.user,
        "user_profile": user_profile,
        "user_services": user_services,
        'average_rating': average_rating,
    }
    return render(request, "other_profile.html", context)


@login_required
def rate_seller(request, username):
    seller = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = UserRatingForm(request.POST)
        if form.is_valid():
            rating_value = int(form.cleaned_data['rating'])

            if request.user == seller:
                # Prevent user from rating themselves
                return redirect('view_other_profile', username=username)

            existing_rating = UserRating.objects.filter(rater=request.user, seller=seller).first()
            if existing_rating:
                existing_rating.rating = rating_value
                existing_rating.save()
                print(f"Updated rating to {rating_value} for seller {seller.username} by {request.user.username}")
            else:
                UserRating.objects.create(rater=request.user, seller=seller, rating=rating_value)
                print(f"Created rating {rating_value} for seller {seller.username} by {request.user.username}")

            return redirect('view_other_profile', username=username)
        else:
            print("Form invalid:", form.errors)
    else:
        form = UserRatingForm()

    context = {
        'form': form,
        'seller': seller,
    }
    return render(request, 'rate_seller.html', context)





@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})



def service_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    services = Service.objects.all()

    if query:
        services = services.filter(title__icontains=query)

    if category:
        services = services.filter(category=category)

    return render(request, 'services/service_list.html', {
        'services': services,
        'query': query,
        'selected_category': category,
    })


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'services/service_detail.html', {'service': service})


@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.owner = request.user
            service.save()
            return redirect('service_detail', pk=service.pk)
    else:
        form = ServiceForm()
    return render(request, 'services/service_form.html', {'form': form})


@login_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.user != service.owner:
        return redirect('service_detail', pk=pk)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_detail', pk=service.pk)
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/service_form.html', {'form': form})


@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.user != service.owner:
        return redirect('service_detail', pk=pk)

    if request.method == 'POST':
        service.delete()
        return redirect('service_list')

    return render(request, 'services/service_confirm_delete.html', {'service': service})


