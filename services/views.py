from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Category, Service, Booking, Review
from .forms import BookingForm, ServiceProfileForm, ReviewForm

def category_list(request):
    categories = Category.objects.all()
    query = request.GET.get('q')  # Grab the search term from the URL
    search_results = None

    if query:
        # Search across service title, description, or category name (case-insensitive)
        search_results = Service.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    return render(request, 'services/category_list.html', {
        'categories': categories,
        'search_results': search_results,
        'query': query
    })

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
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Provider logic: Can Accept/Cancel a Pending job, or Complete an Accepted job
    if getattr(request.user, 'is_provider', False) and request.user == booking.service.provider:
        if (booking.status == 'Pending' and new_status in ['Accepted', 'Cancelled']) or \
           (booking.status == 'Accepted' and new_status == 'Completed'):
            booking.status = new_status
            booking.save()
            messages.success(request, f'Job successfully marked as {new_status}!')
            
    # Customer logic: Can Cancel their own booking if it is still Pending
    elif request.user == booking.customer:
        if booking.status == 'Pending' and new_status == 'Cancelled':
            booking.status = 'Cancelled'
            booking.save()
            messages.success(request, 'Your booking request has been cancelled.')
            
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


@login_required
def add_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Security check: only the customer who booked it can review, and only after completion
    if request.user != booking.customer or booking.status != 'Completed':
        messages.error(request, "You can only review jobs that have been marked as Completed.")
        return redirect('dashboard')

    # Prevent duplicate reviews
    if hasattr(booking, 'review'):
        messages.info(request, "You have already submitted a review for this booking.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.service = booking.service
            review.customer = request.user
            review.save()
            messages.success(request, "Thank you! Your review has been posted.")
            return redirect('dashboard')
    else:
        form = ReviewForm()

    return render(request, 'services/add_review.html', {'form': form, 'booking': booking})