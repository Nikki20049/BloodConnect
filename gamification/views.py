from django.shortcuts import render
from django.db.models import Count, Q
from accounts.models import User
from .models import Badge, UserBadge
from django.shortcuts import render, get_object_or_404


from django.shortcuts import render
from django.db.models import Count, Q
from .models import User  # Assuming User model exists

def leaderboard(request):
    top_donors = User.objects.filter(
        user_type='donor'
    ).annotate(
        total_verified_donations=Count('donations', filter=Q(donations__verification_date__isnull=False))
    ).order_by('-total_verified_donations')[:20]

    # Fetch badges for each donor
    donors_with_badges = []
    for donor in top_donors:
        badges = UserBadge.objects.filter(user=donor).select_related('badge')
        donors_with_badges.append({
            'user': donor,
            'badges': [badge.badge for badge in badges]  # Extract badge names
        })

    context = {
        'top_3_donors': donors_with_badges[:3],  # First 3 members
        'all_donors': donors_with_badges,  # Full list including top 3
    }
    return render(request, 'gamification/leaderboard.html', context)

def badges(request):
    all_badges = Badge.objects.all().order_by('required_donations')
    
    context = {
        'badges': all_badges,
    }
    return render(request, 'gamification/badges.html', context)


def user_badges(request, username):
    user = get_object_or_404(User, username=username)

    # Fetch unlocked badges with related badge details
    unlocked_badges = Badge.objects.filter(userbadge__user=user)

    # Get all available badges
    total_badges = Badge.objects.all()

    context = {
        'profile_user': user,
        'unlocked_badges': unlocked_badges,  # Now passing actual badge objects
        'total_badges': total_badges,
    }
    return render(request, 'gamification/user_badges.html', context)