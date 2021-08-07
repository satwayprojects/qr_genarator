from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django .forms import ModelForm, fields, widgets
from .models import UinLinK,User

class NewUserForm(UserCreationForm):
    password1 = None # Standard django password input
    password2 = None # Standard django password confirmation input
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password',widget=forms.PasswordInput())
    
    def clean(self):
        cleaned_data = super(NewUserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")

            return cleaned_data

    class Meta:
        model = User
        fields = ['username','email']
        labels = {
            'username': ('Enter the Username'),
            
            }



    
class NewUinLinkForm(ModelForm):
    class Meta:
        model= UinLinK
        fields=['imei', 'iccid','uin']
        widgets={
            
            'imei': forms.TextInput(
                attrs={'class':'form-control'}
            ),
            'iccid': forms.TextInput(
                attrs={'class':'form-control'}
            ),
            'uin': forms.TextInput(
                attrs={'class':'form-control' }
            )
        }
