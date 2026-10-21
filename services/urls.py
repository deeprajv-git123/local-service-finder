from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.service_list, name='service_list'),
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('booking/<int:booking_id>/update/<str:new_status>/', views.update_booking_status, name='update_booking_status'),
    path('profile/', views.manage_profile, name='manage_profile'),
]