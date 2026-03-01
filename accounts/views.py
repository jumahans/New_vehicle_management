from django.shortcuts import redirect, render
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            Profile.objects.create(
                user=user,
                role='customer',
                phone_number=form.cleaned_data.get('phone_number'),
                next_of_kin_name=form.cleaned_data.get('next_of_kin_name'),
                next_of_kin_phone=form.cleaned_data.get('next_of_kin_phone')
            )
            messages.success(request, f'Account created! You can now login.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            profile, created = Profile.objects.get_or_create(user=user, defaults={'role': 'customer'})
            
            if profile.role == 'driver':
                return redirect('fleet:dashboard')
            return redirect('fleet:customer-dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('accounts:login')

    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login')


@login_required
def profile_detail(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'accounts/profile_detail.html', {'profile': profile})


@login_required
def profile_update(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        profile.phone_number = request.POST.get('phone_number')
        profile.next_of_kin_name = request.POST.get('next_of_kin_name')
        profile.next_of_kin_phone = request.POST.get('next_of_kin_phone')

        if 'license_front' in request.FILES:
            profile.license_front = request.FILES['license_front']
        if 'license_back' in request.FILES:
            profile.license_back = request.FILES['license_back']

        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('accounts:profile_detail')

    return render(request, 'accounts/profile_update.html', {'profile': profile})


def index_view(request):
    return render(request, 'accounts/index.html')

def more_cars_view(request):
    return render(request, 'accounts/more_cars.html')