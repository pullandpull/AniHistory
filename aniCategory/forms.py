from django import forms

from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    
    username = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'Username'}))
    email = forms.CharField(label = '',  widget=forms.TextInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(label = '' , widget=forms.TextInput(attrs={'placeholder':'Password','type': 'password'}) )
    re_password = forms.CharField(label = '' ,  widget=forms.TextInput(attrs={'placeholder':'Re-Enter Password' ,'type': 'password'}))

    class Meta:
        model = User
        fields = ('username','email','password')

class UserLoginForm(forms.ModelForm):
    
    username = forms.CharField(label = '', widget = forms.TextInput(attrs = {'placeholder': 'Username'}))
    password = forms.CharField(widget = forms.TextInput(attrs = {'type':'password', 'placeholder': 'Password'}) ,label = '')

    class Meta:
        model = User
        fields = ('username','password')