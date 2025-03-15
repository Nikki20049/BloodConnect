from django.urls import path
from . import views

urlpatterns = [
    path('record/', views.record_donation, name='record_donation'),
    path('record/<int:request_id>/', views.record_donation, name='record_donation_for_request'),
    path('history/', views.donation_history, name='donation_history'),
    path('verify/<int:donation_id>/', views.verify_donation, name='verify_donation'),
    path('<int:donation_id>/', views.donation_detail, name='donation_detail'),
]