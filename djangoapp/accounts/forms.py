from django import forms
class LoginForm(forms.Form):
    username=forms.CharField(max_length=150)
    password=forms.CharField(max_length=128,widget=forms.PasswordInput)

class SignUpForm(forms.Form):
    first_name=forms.CharField(max_length=30)
    last_name=forms.CharField(max_length=150)
    username=forms.CharField(max_length=150)
    password=forms.CharField(max_length=200,widget=forms.PasswordInput)
    email=forms.EmailField()




