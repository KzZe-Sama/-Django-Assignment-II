from django import forms
from django.contrib.auth.models import User
class LoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(max_length=128,widget=forms.PasswordInput)

class SignUpForm(forms.Form):
    first_name=forms.CharField(max_length=30)
    last_name=forms.CharField(max_length=150)
    username=forms.CharField(max_length=150)
    email=forms.EmailField()
    password=forms.CharField(max_length=200,widget=forms.PasswordInput)
    confirm_password=forms.CharField(max_length=200,widget=forms.PasswordInput)

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("Email already exists.")
        return self.cleaned_data['email']

    def clean(self):
        password=self.cleaned_data['password']
        confirm_password=self.cleaned_data['confirm_password']
        if password !=confirm_password:
            raise forms.ValidationError("Password doesn't match.")




class Verify(forms.Form):
    code=forms.CharField(max_length=4)
