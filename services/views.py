from django.shortcuts import render, get_object_or_404
from .models import Category, Service

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'services/category_list.html', {'categories': categories})

def service_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    # This grabs all active providers matching the chosen category
    services = Service.objects.filter(category=category, is_active=True)
    return render(request, 'services/service_list.html', {'category': category, 'services': services})