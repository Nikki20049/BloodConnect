from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, DonorProfile
from .forms import UserRegistrationForm, UserProfileForm, DonorProfileForm
from django.shortcuts import render, get_object_or_404
from gamification.models import UserBadge, Badge
from .models import User

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
def profile_view(request, username):
    user = get_object_or_404(User, username=username)

    context = {
        'profile_user': user,
    }

    if user.user_type == 'donor':
        donor_profile = getattr(user, 'donor_profile', None)
        recent_badges = UserBadge.objects.filter(user=user).order_by('-awarded_at')[:3]  # FIXED FIELD NAME
        badge_count = UserBadge.objects.filter(user=user).count()
        # recent_donations = Donation.objects.filter(donor_user=user).order_by('-created_at')[:3]
        # donation_count = Donation.objects.filter(donor_user=user).count()

        context.update({
            'donor_profile': donor_profile,
            'recent_badges': recent_badges,
            'badge_count': badge_count,
            # 'recent_donations': recent_donations,
            # 'donation_count': donation_count,
        })

    return render(request, 'accounts/user_profile.html', context)

@login_required
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=user)

        if user.user_type == 'donor':
            donor_form = DonorProfileForm(request.POST, instance=user.donor_profile)

        if user_form.is_valid() and (user.user_type != 'donor' or donor_form.is_valid()):
            user_form.save()
            if user.user_type == 'donor':
                donor_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user_profile', username=user.username)
    else:
        user_form = UserProfileForm(instance=user)

        if user.user_type == 'donor':
            donor_form = DonorProfileForm(instance=user.donor_profile)

    context = {'user_form': user_form}

    if user.user_type == 'donor':
        context['donor_form'] = donor_form

    return render(request, 'accounts/update_profile.html', context)


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