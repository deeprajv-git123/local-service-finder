from django import forms
from .models import Booking, Service

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your issue or job request here...'})
        }

class ServiceProfileForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['category', 'title', 'description', 'hourly_rate']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe your experience and services...'}),
        }