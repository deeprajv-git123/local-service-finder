from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='category_list', permanent=False), name='home'),
    path('services/', include('services.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', core_views.signup, name='signup'),
]