from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserRegistrationForm

def signup(request):
    # If the user is already logged in, send them away
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log the user in after successful signup
            login(request, user)
            messages.success(request, f"Welcome to Local Service Finder, {user.username}!")
            
            # If they signed up as a provider, take them to create their profile
            if getattr(user, 'is_provider', False):
                return redirect('manage_profile')
            return redirect('dashboard')
    else:
        form = CustomUserRegistrationForm()
        
    return render(request, 'core/signup.html', {'form': form})