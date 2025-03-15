from django import template

register = template.Library()

@register.filter
def percentage_of_max(value, queryset):
    """Calculate percentage of a value compared to the maximum value in a queryset"""
    max_value = max([item['count'] for item in queryset])
    if max_value > 0:
        return (value / max_value) * 100
    return 0

from datetime import timedelta

register = template.Library()

@register.filter
def add_days(value, days):
    """Add a given number of days to a date"""
    if value:
        return value + timedelta(days=int(days))
    return value