from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        if commit:
            user.save()
        return user

class ProviderSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_provider = True
        if commit:
            user.save()
        return user