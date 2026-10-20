from django.contrib import admin
from .models import Category, Service, Booking

admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Booking)