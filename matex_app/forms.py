from datetime import timedelta

from django import forms
from .models import CertificateHolder
from .models import CertificateInfo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields[
            'password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class CertificateHolderForm(forms.ModelForm):
    nhs_number = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Enter NHS Number", "class": "form-control"}), label='NHS number - 10 digits')
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Enter First Name", "class": "form-control"}), label="First name")
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Enter Last name", "class": "form-control"}), label="Last name")
    email = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Enter Email Address", "class": "form-control"}), label="Email address")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = CertificateHolder
        fields = '__all__'


class CertificateInfoForm(forms.ModelForm):
    certificate_start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = CertificateInfo
        fields = '__all__'
        exclude = ['certificate_expiration_date', 'certificate_number']