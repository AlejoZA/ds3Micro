# users/forms.py

from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django import forms
from users.models import OtpCode
from .models import CustomUser
import re

class CustomLoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=256, widget=forms.TextInput(
        attrs={'class': 'form-control small-input', 'placeholder': 'Username or Email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control small-input', 'placeholder': 'Password'}))

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data['username_or_email']
        if "@" in username_or_email:
            validate_email(username_or_email)
            data = {'email': username_or_email}
        else:
            data = {'username': username_or_email}
        try:
            get_user_model().objects.get(**data)
        except get_user_model().DoesNotExist:
            raise ValidationError(
                _('This {} does not exist'.format(list(data.keys())[0])))
        else:
            return username_or_email

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control small-input'}),
        required=True
    )
    last_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control small-input'}),
        required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control small-input'}),
        required=True
    )
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control small-input'}),
        required=True
    )
    cedula = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Cedula', 'class': 'form-control small-input'}),
        required=True
    )
    telefono = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Telefono', 'class': 'form-control small-input'}),
        required=True
    )
    direccion = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Direccion', 'class': 'form-control small-input'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control small-input'})

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[a-zA-Z]+$', first_name):
            raise ValidationError("First name must contain only letters.")
        if len(first_name) > 20:
            raise ValidationError("First name cannot exceed 20 characters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[a-zA-Z]+$', last_name):
            raise ValidationError("Last name must contain only letters.")
        if len(last_name) > 20:
            raise ValidationError("Last name cannot exceed 20 characters.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("This email address already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError("Username can only contain letters, numbers, and underscores.")
        if len(username) > 20:
            raise ValidationError("Username cannot exceed 20 characters.")
        return username

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if not re.match(r'^[0-9]+$', cedula):
            raise ValidationError("Cedula must contain only numbers.")
        if len(cedula) > 20:
            raise ValidationError("Cedula cannot exceed 20 characters.")
        return cedula

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not re.match(r'^[0-9]+$', telefono):
            raise ValidationError("Telefono must contain only numbers.")
        if len(telefono) > 20:
            raise ValidationError("Telefono cannot exceed 20 characters.")
        return telefono

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if len(direccion) > 100:
            raise ValidationError("Direccion cannot exceed 100 characters.")
        return direccion

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "cedula", "telefono", "direccion", "password1", "password2")

class ForgetPasswordEmailCodeForm(forms.Form):
    username_or_email = forms.CharField(
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control small-input', 'placeholder': 'Type your username or email'})
    )

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data['username_or_email']
        if '@' in username_or_email:
            validate_email(username_or_email)
            data = {'email': username_or_email}
        else:
            data = {'username': username_or_email}

        try:
            user = get_user_model().objects.get(**data)
        except get_user_model().DoesNotExist:
            raise ValidationError(
                _('There is no account with this {}').format(list(data.keys())[0])
            )

        if not user.is_active:
            raise ValidationError(_('This account is not active.'))

        return username_or_email

class ChangePasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control small-input',
                'placeholder': 'New password'
            }
        ),
    )
    new_password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control small-input',
                'placeholder': 'Confirm password',
            }
        ),
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data['new_password1']
        password2 = self.cleaned_data['new_password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError(_('Passwords do not match'))
        password_validation.validate_password(password2)
        return password2

class OtpForm(forms.Form):
    otp = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control small-input',
                'placeholder': 'Enter code',
            }
        )
    )

    def clean_otp(self):
        otp_code = self.cleaned_data['otp']
        try:
            OtpCode.objects.get(code=otp_code)
        except OtpCode.DoesNotExist:
            raise ValidationError(
                _('You have entered an incorrect code!')
            )
        else:
            return otp_code

class ProfileEditForm(UserChangeForm):
    password = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'cedula', 'telefono', 'direccion']
    
    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control small-input'})
        # Deshabilitar la edición del campo de correo electrónico
        self.fields['email'].widget.attrs['readonly'] = True

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError("Username can only contain letters, numbers, and underscores.")
        if len(username) > 20:
            raise ValidationError("Username cannot exceed 20 characters.")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[a-zA-Z]+$', first_name):
            raise ValidationError("First name must contain only letters.")
        if len(first_name) > 20:
            raise ValidationError("First name cannot exceed 20 characters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[a-zA-Z]+$', last_name):
            raise ValidationError("Last name must contain only letters.")
        if len(last_name) > 20:
            raise ValidationError("Last name cannot exceed 20 characters.")
        return last_name
