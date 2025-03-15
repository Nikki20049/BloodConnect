from .models import Badge, UserBadge
from notifications.utils import create_notification

def check_and_award_badges(user):
    """
    Check if a user qualifies for any badges and award them
    """
    try:
        donor_profile = user.donor_profile
    except:
        return
    
    total_donations = donor_profile.total_donations
    
    # Get all badges that the user qualifies for but doesn't have yet
    eligible_badges = Badge.objects.filter(
        required_donations__lte=total_donations
    ).exclude(
        id__in=UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
    )
    
    for badge in eligible_badges:
        UserBadge.objects.create(user=user, badge=badge)
        
        # Notify user about new badge
        create_notification(
            recipient=user,
            notification_type='badge',
            title=f'New Badge: {badge.name}',
            message=f'Congratulations! You\'ve earned the {badge.name} badge for your contributions.'
        )