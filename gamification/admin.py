from django.contrib import admin
from .models import Badge, UserBadge

class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'required_donations')
    search_fields = ('name', 'description')

class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'awarded_at')
    list_filter = ('badge', 'awarded_at')
    search_fields = ('user__username', 'badge__name')
    date_hierarchy = 'awarded_at'

admin.site.register(Badge, BadgeAdmin)
admin.site.register(UserBadge, UserBadgeAdmin)