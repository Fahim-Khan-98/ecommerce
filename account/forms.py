from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    mobile = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "mobile", "password1", "password2")

    # PUT IT HERE
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter email'
        })
        self.fields['mobile'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter mobile number'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data['mobile']
            profile.save()

        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fullname', 'phone', 'address', 'city', 'country', 'zipcode', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})