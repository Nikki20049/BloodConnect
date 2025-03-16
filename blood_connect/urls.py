from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import homepage  # Import the homepage view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='home'),  # Use homepage view instead of TemplateView
    path('accounts/', include('accounts.urls')),
    path('requests/', include('blood_requests.urls')),
    path('donations/', include('donations.urls')),
    path('notifications/', include('notifications.urls')),
    path('gamification/', include('gamification.urls')),
    path('dashboard/', include('dashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
