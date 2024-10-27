from django import forms
from django.contrib.auth import authenticate
from main.models import *
import re

class NewUserForm(forms.ModelForm):
    repeat_password = forms.CharField(required=True, widget=forms.PasswordInput)
    agreement = forms.BooleanField(required=True)

    class Meta:
        model = MlakuMlakuUser
        fields = ['name', 'username', 'profile_picture', 'password', 'repeat_password', 'agreement']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and (len(name) < 5 or len(name) > 25):
            raise forms.ValidationError("Name must be between 5 and 25 characters long.")
        if name and not re.match(r"^[A-Za-z\s]+$", name):
            raise forms.ValidationError("Name can only contain letters and spaces.")
        return name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and (len(username) < 5 or len(username) > 20):
            raise forms.ValidationError("Username must be between 5 and 20 characters long.")
        if username and not re.match(r"^[A-Za-z0-9_.]+$", username):
            raise forms.ValidationError("Username can only contain letters, numbers, underscores, and periods.")
        return username

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture is None:
            return 'static/img/noneicon.png'
        return picture

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if (len(password) < 10 or len(password) > 40 or 
                not re.search(r'[A-Z]', password) or
                not re.search(r'[a-z]', password) or
                not re.search(r'[0-9]', password) or
                not re.search(r'[-#_.*]', password)):
                raise forms.ValidationError("Password must be 10-40 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character (-, #, _, ., *).")
        return password

    def clean_repeat_password(self):
        repeat_password = self.cleaned_data.get('repeat_password')
        password = self.cleaned_data.get('password')
        if repeat_password and password and repeat_password != password:
            raise forms.ValidationError("Passwords do not match.")
        return repeat_password
    
    def clean_agreement(self):
        agreement = self.cleaned_data.get('agreement')
        if not agreement:
            raise forms.ValidationError("You must agree to the terms of service.")
        return agreement