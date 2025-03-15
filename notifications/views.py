from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification

@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')
    
    # Mark as read
    unread = user_notifications.filter(is_read=False)
    unread.update(is_read=True)
    
    context = {
        'notifications': user_notifications,
    }
    return render(request, 'notifications/notifications.html', context)

@login_required
def get_unread_notification_count(request):
    count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()
    
    return JsonResponse({'count': count})

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    
    return JsonResponse({'success': True})

@login_required
def mark_all_as_read(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return redirect('notifications')

@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.delete()
    
    return redirect('notifications')