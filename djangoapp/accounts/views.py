from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from .email_backend import EmailBackend
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views import View
from django.contrib import messages
from django.views.generic import TemplateView

# Create your views here.


USER = get_user_model()


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/accounts/profile/')
        form = LoginForm()
        return render(request,
                      'accounts/login.html',
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            back = EmailBackend()

            user = back.authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user:
                print(" a user is found", user)
                login(request, user)
                return redirect('/accounts/profile/')
            else:
                messages.error(request, "Login Invalid")
                return redirect('/accounts/login/')


# Soon to be implememnted on class views
@login_required()
def profile_view(request):
    return render(request, 'accounts/profile.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/accounts/login/')


class SignupView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            from django.contrib.auth.models import User
            user = USER(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],

            )
            user.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('/accounts/login/')
        return render(request, 'accounts/register.html', {'form': form})
