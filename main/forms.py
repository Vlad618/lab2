from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Rating, NewsletterSubscription

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.Select(choices=[(i, f"{i} ★") for i in range(1, 6)], attrs={'class': 'form-select'}),
        }
        labels = {
            'score': 'Оцініть модифікацію',
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Введіть ваш Email', 'class': 'form-input'}),
        }
        labels = {
            'email': '',
        }

class PaymentForm(forms.Form):
    card_number = forms.CharField(
        label="Номер карти",
        max_length=19,
        widget=forms.TextInput(attrs={'placeholder': '0000 0000 0000 0000', 'class': 'form-input'})
    )
    expiry_date = forms.CharField(
        label="Термін дії (ММ/РР)",
        max_length=5,
        widget=forms.TextInput(attrs={'placeholder': 'ММ/РР', 'class': 'form-input'})
    )
    cvv = forms.CharField(
        label="CVV",
        max_length=3,
        widget=forms.PasswordInput(attrs={'placeholder': '***', 'class': 'form-input'})
    )
