from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_blood_request, name='create_blood_request'),
    path('<int:request_id>/', views.view_request, name='view_request'),
    path('<int:request_id>/update-status/', views.update_request_status, name='update_request_status'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('search/', views.search_requests, name='search_requests'),
]