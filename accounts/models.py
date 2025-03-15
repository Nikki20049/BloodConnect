from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    USER_TYPES = (
        ('regular', 'Regular User'),
        ('donor', 'Blood Donor'),
        ('admin', 'Administrator'),
        ('ngo', 'NGO'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='regular')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return self.username

class BloodGroup(models.Model):
    name = models.CharField(max_length=5)  # A+, B-, O+, etc.
    
    def __str__(self):
        return self.name

class DonorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor_profile')
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.SET_NULL, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    medical_conditions = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    last_donation_date = models.DateField(null=True, blank=True)
    total_donations = models.PositiveIntegerField(default=0)
    
    def can_donate(self):
        if not self.last_donation_date:
            return True
        
        # Check if 3 months have passed since last donation
        days_since_donation = (timezone.now().date() - self.last_donation_date).days
        return days_since_donation >= 90
    
    def __str__(self):
        return f"{self.user.username}'s Donor Profile"