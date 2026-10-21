from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # We add 'is_provider' so users can choose their account type at signup
        fields = ('username', 'email', 'is_provider')
        help_texts = {
            'is_provider': 'Check this box if you want to offer services on our platform.',
        }