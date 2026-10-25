from django.db import models
from django.conf import settings
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Service(models.Model):
    # Links this profile to the specific user who created it
    provider = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='service_profile')
    
    # Links this profile to one of the categories you just created
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='services')
    
    title = models.CharField(max_length=200, help_text="e.g., Expert Residential Plumber")
    description = models.TextField()
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.provider.username}"

    @property
    def average_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else None

    @property
    def review_count(self):
        return self.reviews.count()

class Booking(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    
    # Links to the customer requesting the job
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings_made')
    
    # Links to the provider's specific service
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings_received')
    
    # The customer explains what they need
    description = models.TextField(help_text="Please describe the job or issue.")
    
    # Tracks where the job is in the pipeline
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.service.title} ({self.status})"


# Add this at the bottom of services/models.py:

class Review(models.Model):
    RATING_CHOICES = [
        (5, '★★★★★ (5/5)'),
        (4, '★★★★☆ (4/5)'),
        (3, '★★★☆☆ (3/5)'),
        (2, '★★☆☆☆ (2/5)'),
        (1, '★☆☆☆☆ (1/5)'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} Stars - {self.service.title} by {self.customer.username}"
    