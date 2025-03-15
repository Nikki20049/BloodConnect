from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from accounts.models import User, DonorProfile
from blood_requests.models import BloodRequest
from donations.models import Donation

@login_required
def donor_dashboard(request):
    if request.user.user_type != 'donor':
        messages.error(request, 'You do not have access to the donor dashboard.')
        return redirect('home')
    
    try:
        donor_profile = request.user.donor_profile
    except DonorProfile.DoesNotExist:
        return redirect('complete_donor_profile')
    
    matching_requests = BloodRequest.objects.filter(
        blood_group=donor_profile.blood_group,
        status='pending',
        needed_by__gte=timezone.now()
    ).order_by('urgency', 'needed_by')
    
    recent_donations = Donation.objects.filter(donor=request.user).order_by('-donation_date')[:5]
    
    # Get user badges
    badges = request.user.badges.all().select_related('badge')
    
    context = {
        'donor_profile': donor_profile,
        'matching_requests': matching_requests,
        'recent_donations': recent_donations,
        'badges': badges,
        'can_donate': donor_profile.can_donate(),
    }
    return render(request, 'dashboard/donor_dashboard.html', context)

@login_required
def admin_dashboard(request):
    if request.user.user_type not in ['admin', 'ngo']:
        messages.error(request, 'You do not have access to this dashboard.')
        return redirect('home')
    
    # Statistics
    pending_requests = BloodRequest.objects.filter(status='pending').count()
    fulfilled_requests = BloodRequest.objects.filter(status='fulfilled').count()
    total_donations = Donation.objects.count()
    verified_donations = Donation.objects.filter(verification_date__isnull=False).count()
    total_donors = User.objects.filter(user_type='donor').count()
    
    # Recent activity
    recent_requests = BloodRequest.objects.all().order_by('-created_at')[:10]
    recent_donations = Donation.objects.all().order_by('-donation_date')[:10]
    
    # Donations pending verification
    pending_verifications = Donation.objects.filter(verification_date__isnull=True).order_by('-donation_date')
    
    # Blood group statistics
    blood_group_stats = BloodRequest.objects.values('blood_group__name').annotate(
        count=Count('id')
    ).order_by('blood_group__name')
    
    context = {
        'pending_requests': pending_requests,
        'fulfilled_requests': fulfilled_requests,
        'total_donations': total_donations,
        'verified_donations': verified_donations,
        'total_donors': total_donors,
        'recent_requests': recent_requests,
        'recent_donations': recent_donations,
        'pending_verifications': pending_verifications,
        'blood_group_stats': blood_group_stats,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def user_dashboard(request):
    if request.user.user_type == 'donor':
        return redirect('donor_dashboard')
    elif request.user.user_type in ['admin', 'ngo']:
        return redirect('admin_dashboard')
    
    # Regular user dashboard
    my_requests = BloodRequest.objects.filter(requester=request.user).order_by('-created_at')
    
    context = {
        'my_requests': my_requests,
    }
    return render(request, 'dashboard/user_dashboard.html', context)