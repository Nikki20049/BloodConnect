from django.db import models
from django.utils import timezone
from accounts.models import User, BloodGroup

class BloodRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('fulfilled', 'Fulfilled'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    )
    
    URGENCY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_requests')
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.CASCADE)
    units_needed = models.PositiveIntegerField(default=1)
    hospital_name = models.CharField(max_length=255)
    hospital_address = models.TextField() 
    patient_name = models.CharField(max_length=255) 
    patient_age = models.PositiveIntegerField()
    reason = models.TextField()
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    needed_by = models.DateTimeField()
    
    def is_expired(self):
        return timezone.now() > self.needed_by
    
    def save(self, *args, **kwargs):
        if self.is_expired() and self.status == 'pending':
            self.status = 'expired'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Blood Request for {self.blood_group} by {self.requester.username}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.blood_request}"