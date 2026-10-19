from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomerSignUpForm, ProviderSignUpForm

def register_customer(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Logs the user in immediately after signup
            return redirect('/') # Redirects to home page (we'll build this soon)
    else:
        form = CustomerSignUpForm()
    return render(request, 'accounts/register_customer.html', {'form': form})

def register_provider(request):
    if request.method == 'POST':
        form = ProviderSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = ProviderSignUpForm()
    return render(request, 'accounts/register_provider.html', {'form': form})