from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")


class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        validators=[validate_email],  # Ensure email is unique
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'})
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Username'})
    )
    date_of_birth = forms.DateField(
        widget=DateInput(attrs={'placeholder': 'Enter Date of Birth'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True  # Mark the user as a customer
        if commit:
            user.save()
            # Create a customer profile and associate it with the user
            Customer.objects.create(user=user, birth=self.cleaned_data['date_of_birth'])
        return user

class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        validators=[validate_email],  # Ensure email is unique
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'})
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Username'})
    )
    field = forms.ChoiceField(
        choices=Company._meta.get_field('field').choices,  # Use choices from the Company model
        widget=forms.Select(attrs={'placeholder': 'Select Field of Work'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'field']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True  # Mark the user as a company
        if commit:
            user.save()
            # Create a company profile and associate it with the user
            Company.objects.create(user=user, field=self.cleaned_data['field'])
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Email', 'autocomplete': 'off'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'})
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        # Check if both email and password were provided
        if email and password:
            # Authenticate the user
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password.")
        
        return self.cleaned_data


# class UserLoginForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super(UserLoginForm, self).__init__(*args, **kwargs)

#     email = forms.EmailField(widget=forms.TextInput(
#         attrs={'placeholder': 'Enter Email'}))
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

#     def __init__(self, *args, **kwargs):
#         super(UserLoginForm, self).__init__(*args, **kwargs)
#         self.fields['email'].widget.attrs['autocomplete'] = 'off'
