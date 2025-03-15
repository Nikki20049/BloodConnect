from django.urls import path
from . import views

urlpatterns = [
    path('', views.notifications, name='notifications'),
    path('count/', views.get_unread_notification_count, name='notification_count'),
    path('mark-read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
]