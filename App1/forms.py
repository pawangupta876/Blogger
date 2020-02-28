from django import forms
from App1.models import UserProfileInfo, User_Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('username', 'password',)

class UserProfileForm(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        exclude = ['user']

class User_Post_Form(forms.ModelForm):

    class Meta():
        model = User_Post
        fields = ('image',)