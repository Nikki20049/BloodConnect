from django import forms
from .models import BloodRequest, Comment

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['blood_group', 'units_needed', 'hospital_name', 'hospital_address', 
                 'patient_name', 'patient_age', 'reason', 'urgency', 'needed_by']
        widgets = {
            'needed_by': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
            'hospital_address': forms.Textarea(attrs={'rows': 2}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write a comment...'}),
        }

class RequestStatusForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['status']