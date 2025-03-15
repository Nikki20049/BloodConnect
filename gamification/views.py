from django.shortcuts import render
from django.db.models import Count, Q
from accounts.models import User
from .models import Badge, UserBadge



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
    user = User.objects.get(username=username)
    user_badges = UserBadge.objects.filter(user=user).select_related('badge')
    
    context = {
        'profile_user': user,
        'user_badges': user_badges,
    }
    return render(request, 'gamification/user_badges.html', context)