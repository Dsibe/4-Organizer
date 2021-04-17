from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *


class UniquePlanUserRegisterForm(UserCreationForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'class': 'name-form'}))
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'last-name-form'}))

    months_amount = forms.IntegerField(min_value=1, initial=1)
    machines_amount = forms.IntegerField(min_value=1, initial=1)

    class Meta:
        model = User
        fields = [
            'username', 'months_amount', 'machines_amount', 'first_name',
            'last_name', 'password1', 'password2'
        ]


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'class': 'name-form'}))
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'last-name-form'}))
    period = forms.CharField(
        label='Select a plan:',
        widget=forms.Select(choices=(('1', '1 month - $4.99'),
                                     ('3', '3 months - $12.99'),
                                     ('6', '6 months - $19.99'),
                                     ('12', '1 year - $24.99, -60% discount!'),
                                     ('0', 'FOREVER - $499.99')),
                            attrs={'class': 'form-control'}),
        initial='1')

    class Meta:
        model = User
        fields = [
            'username', 'period', 'first_name', 'last_name', 'password1',
            'password2'
        ]


class UserUpdateForm(ModelForm):
    new_username = forms.CharField(required=True, initial='username')
    first_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'class': 'name-form'}))
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'last-name-form'}))

    class Meta:
        model = User
        fields = ['new_username', 'first_name', 'last_name']
