from django.db import models
from accounts.models import User
from blood_requests.models import BloodRequest
from donations.models import Donation

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('request', 'Blood Request'),
        ('donation', 'Donation'),
        ('badge', 'Badge Earned'),
        ('comment', 'Comment'),
        ('system', 'System Notification'),
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    related_request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, null=True, blank=True)
    related_donation = models.ForeignKey(Donation, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.title}"