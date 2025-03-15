from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, DonorProfile
from .forms import UserRegistrationForm, UserProfileForm, DonorProfileForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            user.user_type = user_type
            user.save()
            
            if user_type == 'donor':
                DonorProfile.objects.create(user=user)
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            
            if user_type == 'donor':
                return redirect('complete_donor_profile')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def user_profile(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('user_profile')
    else:
        user_form = UserProfileForm(instance=request.user)
    
    if request.user.user_type == 'donor':
        try:
            donor_profile = request.user.donor_profile
        except DonorProfile.DoesNotExist:
            donor_profile = None
        
        context = {
            'user_form': user_form,
            'donor_profile': donor_profile,
        }
        return render(request, 'accounts/donor_profile.html', context)
    else:
        context = {
            'user_form': user_form,
        }
        return render(request, 'accounts/user_profile.html', context)

@login_required
def complete_donor_profile(request):
    try:
        profile = request.user.donor_profile
    except DonorProfile.DoesNotExist:
        profile = DonorProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = DonorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your donor profile has been updated!')
            return redirect('donor_dashboard')
    else:
        form = DonorProfileForm(instance=profile)
    
    return render(request, 'accounts/complete_donor_profile.html', {'form': form})

@login_required
def toggle_availability(request):
    if request.user.user_type != 'donor':
        messages.error(request, 'Only donors can change availability status.')
        return redirect('home')
    
    try:
        profile = request.user.donor_profile
        profile.is_available = not profile.is_available
        profile.save()
        
        status = "available" if profile.is_available else "unavailable"
        messages.success(request, f'You are now {status} for donations.')
    except DonorProfile.DoesNotExist:
        messages.error(request, 'Donor profile not found.')
    
    return redirect('user_profile')