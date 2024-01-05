from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Comment

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = Comment
        fields = ('content')
