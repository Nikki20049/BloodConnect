from .models import Notification
from accounts.models import User

def create_notification(recipient, notification_type, title, message, related_request=None, related_donation=None):
    """
    Create a notification for a user
    """
    notification = Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        related_request=related_request,
        related_donation=related_donation
    )
    return notification

def notify_donors(blood_request):
    """
    Notify donors with matching blood group about a new blood request
    """
    matching_donors = User.objects.filter(
        user_type='donor',
        donor_profile__blood_group=blood_request.blood_group,
        donor_profile__is_available=True
    )
    
    for donor in matching_donors:
        create_notification(
            recipient=donor,
            notification_type='request',
            title='Urgent Blood Request',
            message=f'Someone needs {blood_request.blood_group} blood at {blood_request.hospital_name}. Urgency: {blood_request.get_urgency_display()}',
            related_request=blood_request
        )