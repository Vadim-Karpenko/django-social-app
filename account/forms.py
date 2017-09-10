from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.forms import SelectDateWidget
import time

class LoginForm(forms.Form):
    username = forms.CharField(label="Username or e-mail")
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)

class ProfileEditForm(forms.ModelForm):
    # make tuple looks like ['1900', '1901', ... '2017']
    BIRTH_YEAR_CHOICES = []
    i = 1900
    while i <= time.gmtime().tm_year:
        BIRTH_YEAR_CHOICES.append(str(i))
        i += 1

    date_of_birth = forms.DateField(
        widget=SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
            years=BIRTH_YEAR_CHOICES,
        ),

    )
    class Meta:
        model = Profile
        fields = ( 'date_of_birth', 'photo')
