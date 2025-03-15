from django.contrib import admin
from .models import Donation

class DonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'donor', 'blood_request', 'donation_date', 'units', 'hospital', 'verified_by', 'verification_date')
    list_filter = ('donation_date', 'verification_date')
    search_fields = ('donor__username', 'hospital')
    date_hierarchy = 'donation_date'
    raw_id_fields = ('donor', 'blood_request', 'verified_by')

admin.site.register(Donation, DonationAdmin)