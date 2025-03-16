from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .models import Donation
from .forms import DonationForm
from blood_requests.models import BloodRequest
from accounts.models import DonorProfile
from notifications.utils import create_notification
from gamification.utils import check_and_award_badges

@login_required
def record_donation(request, request_id=None):
    if request.user.user_type != 'donor':
        messages.error(request, 'Only donors can record donations.')
        return redirect('home')
    
    blood_request = None
    if request_id:
        blood_request = get_object_or_404(BloodRequest, id=request_id)
    
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            
            if blood_request:
                donation.blood_request = blood_request
            
            donation.save()
            
            # Update donor profile
            try:
                donor_profile = request.user.donor_profile
                donor_profile.last_donation_date = timezone.now().date()
                donor_profile.total_donations += 1
                donor_profile.save()
            except DonorProfile.DoesNotExist:
                pass
            
            # Check for badges
            check_and_award_badges(request.user)
            
            # Notify requester if applicable
            if blood_request:
                create_notification(
                    recipient=blood_request.requester,
                    notification_type='donation',
                    title='Someone donated for your request!',
                    message=f'{request.user.username} has donated blood for your request.',
                    related_request=blood_request,
                    related_donation=donation
                )
            
            messages.success(request, 'Donation recorded successfully! Thank you for your contribution.')
            return redirect('donor_dashboard')
    else:
        initial_data = {}
        if blood_request:
            initial_data = {
                'units': 1,
                'hospital': blood_request.hospital_name,
            }
        form = DonationForm(initial=initial_data)
    
    context = {
        'form': form,
        'blood_request': blood_request,
    }
    return render(request, 'donations/record_donation.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Donation

@login_required
def donation_history(request):
    # Admins and NGOs can see all donations, Donors can only see their own
    if request.user.user_type == 'donor':
        donations = Donation.objects.filter(donor=request.user).order_by('-donation_date')
    elif request.user.user_type in ['admin', 'ngo']:
        donations = Donation.objects.all().order_by('-donation_date')

        # Filtering options
        search_query = request.GET.get('search', '')
        status_filter = request.GET.get('status', '')

        if search_query:
            donations = donations.filter(
                Q(donor__username__icontains=search_query) |
                Q(hospital__icontains=search_query)
            )

        if status_filter:
            if status_filter == 'verified':
                donations = donations.filter(verification_date__isnull=False)
            elif status_filter == 'pending':
                donations = donations.filter(verification_date__isnull=True)

    else:
        messages.error(request, 'You do not have permission to view donation history.')
        return redirect('home')

    context = {
        'donations': donations,
    }
    return render(request, 'donations/donation_history.html', context)


@login_required
def verify_donation(request, donation_id):
    if request.user.user_type not in ['admin', 'ngo']:
        messages.error(request, 'You do not have permission to verify donations.')
        return redirect('home')
    
    donation = get_object_or_404(Donation, id=donation_id)
    
    if donation.verification_date:
        messages.warning(request, 'This donation has already been verified.')
    else:
        donation.verified_by = request.user
        donation.verification_date = timezone.now()
        donation.save()
        
        # If this donation is for a blood request, check if request is fulfilled
        if donation.blood_request:
            total_donated = Donation.objects.filter(
                blood_request=donation.blood_request,
                verification_date__isnull=False
            ).aggregate(total=Sum('units'))['total'] or 0
            
            # if total_donated >= donation.blood_request.units_needed:  return 0
            
            if total_donated >= donation.blood_request.units_needed:
                donation.blood_request.status = 'fulfilled'
                donation.blood_request.save()
                
                # Notify the requester
                create_notification(
                    recipient=donation.blood_request.requester,
                    notification_type='request',
                    title='Your blood request has been fulfilled!',
                    message=f'Your blood request has been fulfilled with the required units.',
                    related_request=donation.blood_request
                )
        
        # Notify the donor
        create_notification(
            recipient=donation.donor,
            notification_type='donation',
            title='Your donation has been verified!',
            message=f'Your donation on {donation.donation_date.date()} has been verified by {request.user.username}.',
            related_donation=donation
        )
        
        messages.success(request, 'Donation verified successfully.')
    
    return redirect('admin_dashboard')

@login_required
def donation_detail(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    
    # Check if user has permission to view this donation
    if request.user != donation.donor and request.user.user_type not in ['admin', 'ngo']:
        if donation.blood_request and request.user != donation.blood_request.requester:
            messages.error(request, 'You do not have permission to view this donation.')
            return redirect('home')
    
    context = {
        'donation': donation,
    }
    return render(request, 'donations/donation_detail.html', context)