from django.contrib import admin
from .models import BloodRequest, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'requester', 'blood_group', 'units_needed', 'hospital_name', 'urgency', 'status', 'created_at', 'needed_by')
    list_filter = ('blood_group', 'urgency', 'status', 'created_at')
    search_fields = ('requester__username', 'hospital_name', 'patient_name')
    date_hierarchy = 'created_at'
    inlines = [CommentInline]

admin.site.register(BloodRequest, BloodRequestAdmin)
admin.site.register(Comment)