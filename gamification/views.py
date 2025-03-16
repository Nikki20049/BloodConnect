from django.shortcuts import render
from django.db.models import Count, Q
from accounts.models import User
from .models import Badge, UserBadge
from django.shortcuts import render, get_object_or_404


def leaderboard(request):
    top_donors = User.objects.filter(
        user_type='donor'
    ).annotate(
        total_verified_donations=Count('donations', filter=Q(donations__verification_date__isnull=False))
    ).order_by('-total_verified_donations')[:20]
    
    context = {
        'top_donors': top_donors,
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

    # Get unlocked badges (extract only Badge objects)
    unlocked_badges = Badge.objects.filter(userbadge__user=user)
    
    # Convert unlocked badges into a list of IDs
    unlocked_badge_ids = set(unlocked_badges.values_list('id', flat=True))

    # Get all available badges
    total_badges = Badge.objects.all()

    context = {
        'profile_user': user,
        'unlocked_badge_ids': unlocked_badge_ids,  # Pass only badge IDs
        'total_badges': total_badges,
    }
    return render(request, 'gamification/user_badges.html', context)