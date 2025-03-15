from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, BloodGroup, DonorProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'address', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'address', 'profile_picture')}),
    )

class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'is_available', 'last_donation_date', 'total_donations')
    list_filter = ('blood_group', 'is_available')
    search_fields = ('user__username', 'user__email')

admin.site.register(User, CustomUserAdmin)
admin.site.register(BloodGroup)
admin.site.register(DonorProfile, DonorProfileAdmin)