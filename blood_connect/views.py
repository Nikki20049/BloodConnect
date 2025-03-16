from django.shortcuts import render
from django.db.models import Count, Q
from blood_requests.models import BloodRequest
from donations.models import Donation
from accounts.models import User

def homepage(request):
    urgent_requests = BloodRequest.objects.filter(urgency__gte=2).order_by('-created_at')[:3]
    recent_donations = Donation.objects.all().order_by('-donation_date')[:3]

    # ✅ Fetch top donors with donations_count
    top_donors = User.objects.filter(
        user_type='donor'
    ).annotate(
        donations_count=Count('donations')  # ✅ Count all donations for this donor
    ).order_by('-donations_count')[:5]  # ✅ Order by highest donation count

    context = {
        'urgent_requests': urgent_requests,
        'recent_donations': recent_donations,
        'top_donors': top_donors,
    }
    return render(request, 'home.html', context)
