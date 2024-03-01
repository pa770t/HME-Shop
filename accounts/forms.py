from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm as PCForm
from .models import OTP, User as CustomUser
from .backends import EmailOrPhoneModelBackend
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator, validate_email

User = get_user_model()

class RegisterForm(UserCreationForm):
    # (UserCreationForm.Meta)
    email_or_phone = forms.CharField(max_length=255)
    class Meta:
        model = CustomUser
        fields = ['name', 'email_or_phone',  'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        email_or_phone = cleaned_data.get('email_or_phone')

        # Check if the input is an email address
        email_validator = EmailValidator()
        try:
            email_validator(email_or_phone)
            # If it's a valid email, populate the email field
            cleaned_data['email'] = email_or_phone
            cleaned_data['phone_number'] = None
            try:
                User.objects.get(email=cleaned_data['email'])
                self.add_error('email_or_phone', 'User with this email already exists!')
            except:
                pass
        except ValidationError:
            # If it's not a valid email, assume it's a phone number
            phone_validator = RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+99999999'. Up to 15 digits allowed."
            )
            try:
                phone_validator(email_or_phone)
                # If it's a valid phone number, populate the phone_number field
                cleaned_data['phone_number'] = email_or_phone
                cleaned_data['email'] = None
            except:
                # If it's not a valid phone number, raise a validation error
                try:
                    User.objects.get(email=cleaned_data['email'])
                    raise forms.ValidationError('User with this email already exists!')
                except:
                    raise forms.ValidationError("Invalid email or phone number.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # Save logic based on whether it's an email or phone number
        if self.cleaned_data.get('email'):
            user.email = self.cleaned_data['email']
            user.phone_number = None
        elif self.cleaned_data.get('phone_number'):
            user.phone_number = self.cleaned_data['phone_number']
            user.email = None

        if commit:
            user.save()

        return user

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=255)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if '@' in username:
            try:
                validate_email(username)
            except ValidationError:
                raise forms.ValidationError('Enter a valid email address.')
        else:
            phone_validator = RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
            try:
                phone_validator(username)
            except ValidationError:
                raise forms.ValidationError('Enter a valid phone number')
        
        return username

class ProfileSettingForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'phone_number', 'email', 'profile_photo']

class PasswordChangeForm(PCForm):
    old_password = forms.CharField(required=True, widget=forms.PasswordInput(), error_messages={'required': 'You must privide your old password!'})
    new_password1 = forms.CharField(required=True, widget=forms.PasswordInput(), error_messages={'required': 'You must privide your new password!'})
    new_password2 = forms.CharField(required=True, widget=forms.PasswordInput(), error_messages={'required': 'You must privide your new confirm password!'})

class OTPForm(forms.ModelForm):
    class Meta:
        model = OTP
        fields = ['otp']
