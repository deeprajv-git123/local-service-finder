from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Service, Booking
from .forms import BookingForm, ServiceProfileForm

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'services/category_list.html', {'categories': categories})

def service_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    services = Service.objects.filter(category=category, is_active=True)
    return render(request, 'services/service_list.html', {'category': category, 'services': services})

# @login_required forces users to log in before they can see this page
@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # commit=False pauses the save so we can attach the user and service manually
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.service = service
            booking.save()
            
            # Trigger the success flash message
            messages.success(request, 'Your booking request has been sent successfully!')
            return redirect('dashboard') 
    else:
        form = BookingForm()
        
    return render(request, 'services/book_service.html', {'form': form, 'service': service})

@login_required
def dashboard(request):
    # Check if the user is a provider
    if getattr(request.user, 'is_provider', False):
        try:
            # Get bookings for their specific service profile
            bookings = request.user.service_profile.bookings_received.all()
        except:
            # If the provider hasn't created a service profile yet
            bookings = []
    else:
        # Customers see the bookings they requested
        bookings = request.user.bookings_made.all()
        
    return render(request, 'services/dashboard.html', {'bookings': bookings})

@login_required
def update_booking_status(request, booking_id, new_status):
    # Find the exact booking in the database
    booking = get_object_or_404(Booking, id=booking_id)
    
    # SECURITY CHECK: Make sure the logged-in user is the provider for this specific job
    if getattr(request.user, 'is_provider', False) and request.user == booking.service.provider:
        # Check if the new status is valid based on our STATUS_CHOICES
        if new_status in ['Accepted', 'Completed', 'Cancelled']:
            booking.status = new_status
            booking.save()

            # Trigger the status update flash message
            messages.success(request, f'Job successfully marked as {new_status}!')

    # Refresh the dashboard page
    return redirect('dashboard')


@login_required
def manage_profile(request):
    # Only allow providers to access this page
    if not getattr(request.user, 'is_provider', False):
        messages.error(request, "Only registered providers can create a service profile.")
        return redirect('category_list')

    # Check if the provider already has a profile
    try:
        service_profile = request.user.service_profile
    except:
        service_profile = None

    if request.method == 'POST':
        # Pass the existing profile (if it exists) to the form so it updates instead of duplicating
        form = ServiceProfileForm(request.POST, instance=service_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.provider = request.user
            profile.save()
            
            messages.success(request, 'Service profile saved successfully!')
            return redirect('dashboard')
    else:
        form = ServiceProfileForm(instance=service_profile)
        
    return render(request, 'services/manage_profile.html', {'form': form})
