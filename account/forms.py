from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    mobile = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "mobile", "password1", "password2")