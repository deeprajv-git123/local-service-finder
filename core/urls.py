from django.contrib import admin
from django.urls import path, include
from core import views as core_views  # <-- Add this import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('services/', include('services.urls')),
    
    # Auth routes
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', core_views.signup, name='signup'), # <-- Add this line
]