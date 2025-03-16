from django import template

register = template.Library()

@register.filter
def percentage_of_max(value, max_value):
    """Returns the percentage of `value` relative to `max_value` (0-100%)."""
    try:
        value = float(value)
        max_value = float(max_value)
        if max_value == 0:
            return 0  # Avoid division by zero
        return (value / max_value) * 100
    except (ValueError, TypeError):
        return 0  # Return 0 if invalid input
import datetime

@register.filter
def add_days(value, days):
    """Adds the specified number of days to a given date."""
    if isinstance(value, datetime.date):
        return value + datetime.timedelta(days=days)
    return value  # Return as is if value is not a date