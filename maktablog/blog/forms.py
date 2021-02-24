from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import UserInfo


class SignUpForm(UserCreationForm):
    """
    This form inherited from UserCreationForm default django for validations,
    this form used for sign-up user in site
    """
    alias_name = forms.CharField(label='نام مستعار', max_length=100, help_text='نام مستعار')
    phone_number = forms.CharField(label='شماره تلفن', max_length=20, required=False)
    image = forms.ImageField(label="عکس پروفایل", required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'alias_name', 'image', 'phone_number',
                  'email', 'password1', 'password2',)


class UserInfoUpdateForm(forms.ModelForm):
    """
    In profile model, this class designed for handle extra data that saved for users
    for example alias_name,phone_number,image saved in this model
    """

    class Meta:
        model = UserInfo
        fields = ['alias_name', 'phone_number', 'image', ]


class UserUpdateForm(forms.ModelForm):
    """
    This form desined for User model django that is default
    """

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
