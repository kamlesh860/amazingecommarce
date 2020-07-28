from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, TextInput, EmailField
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    # email=forms.EmailField
    email= forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model=User
        fields=['first_name','last_name','email']


        


