from django.db import models
from django.utils import timezone
from accounts.models import User
from blood_requests.models import BloodRequest

class Donation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    blood_request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name='donations', null=True, blank=True)
    donation_date = models.DateTimeField(default=timezone.now)
    units = models.PositiveIntegerField(default=1)
    hospital = models.CharField(max_length=255)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_donations')
    verification_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Donation by {self.donor.username} on {self.donation_date.date()}"