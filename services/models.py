from django.db import models
from django.conf import settings

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
    