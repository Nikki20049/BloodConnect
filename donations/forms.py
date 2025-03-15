from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['units', 'hospital', 'donation_date']
        widgets = {
            'donation_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }