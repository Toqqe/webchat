from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser  


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=60, required=True)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    is_guest = forms.BooleanField(label="Enter as a guest: ", widget=forms.CheckboxInput(), required=False)

    username.widget.attrs['class'] = "form-control"
    password.widget.attrs['class'] = "form-control"

class CreateNewChannel(forms.Form):
    channel_name = forms.CharField(max_length=30, required=True)
    is_private = forms.BooleanField(label="Private?", widget=forms.CheckboxInput(), required=False, initial=False)

    channel_name.widget.attrs['class'] = "form-control"



class RegistrationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class':'form-control'})
        self.fields['password1'].widget.attrs.update({'class':'form-control'})
        self.fields['password2'].widget.attrs.update({'class':'form-control'})

class UpdateUserForm(forms.ModelForm):

    username = forms.CharField(max_length=60, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']