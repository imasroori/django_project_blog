from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import UserInfo


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='نام', max_length=100, help_text='نام')
    last_name = forms.CharField(label='نام خانوادگی', max_length=100, help_text='نام خانوادگی')
    email = forms.EmailField(label='ایمیل', max_length=150, help_text='ایمیل')
    phone_number = forms.CharField(label='شماره تلفن', max_length=20, required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'image', 'phone_number',
                  'email', 'password1', 'password2',)


class UserInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['first_name', 'last_name', 'alias_name', 'phone_number', 'image', ]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
