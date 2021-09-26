import hashlib
import random

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from django.core.exceptions import ValidationError

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control py-4',
               'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control py-4',
               'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control py-4',
               'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control py-4',
               'placeholder': 'Введите адрес эл. почты'}))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control py-4',
               'placeholder': 'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control py-4',
               'placeholder': 'Введите фамилию'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control py-4',
               'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control py-4',
               'placeholder': 'Подтвердите пароль'}))
    age = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control py-4',
               'placeholder': 'Введите возраст'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2', 'age')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf-8')).hexdigest()
        user.save()
        return user

    def clean_email(self):
        if self.cleaned_data["email"] in User.objects.values_list("email", flat=True):
            raise ValidationError(
                "Такой email-адрес уже существует!",
                params={'value': self.cleaned_data["email"]},
            )
        return self.cleaned_data["email"]


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control py-4', 'readonly': True}))
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control py-4',
               'readonly': True}))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'custom-file-input'}), required=False)
    age = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control py-4'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'image', 'age')
