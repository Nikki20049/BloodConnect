from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, DonorProfile

class UserRegistrationForm(UserCreationForm):
    USER_TYPES = (
        ('regular', 'Regular User'),
        ('donor', 'Blood Donor'),
    )
    
    user_type = forms.ChoiceField(choices=USER_TYPES, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'profile_picture']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class DonorProfileForm(forms.ModelForm):
    class Meta:
        model = DonorProfile
        fields = ['blood_group', 'weight', 'medical_conditions', 'is_available']
        widgets = {
            'medical_conditions': forms.Textarea(attrs={'rows': 3}),
        }